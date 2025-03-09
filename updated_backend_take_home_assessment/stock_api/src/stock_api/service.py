import requests
import logging
from fastapi import HTTPException
import datetime
from datetime import timedelta, date
import requests_cache

class AlphaVantageAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.host = "https://www.alphavantage.co/query"
        self.session = requests_cache.CachedSession(
            "alpha_vantage_cache", expire_after=timedelta(minutes=10)
        )

    def get_stock_data(self, symbol: str, date: str):
        output_size = self.determine_output_size_by_date(date)
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": output_size,
            "apikey": self.api_key,
        }
        response = self.session.get(self.host, params=params)
        if getattr(response, "from_cache", False):
            logging.info("Serving from cache")
        else:
            logging.info("Fetching from API")

        data = response.json()
        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            logging.info(data)
            raise HTTPException(status_code=response.status_code, detail=f"Could not find {symbol} at {date} - {response.content}")
        return time_series

    def lookup(self, symbol: str, date: str):
        time_series = self.get_stock_data(symbol, date)
        stock_data = time_series[date]
        if not stock_data:
            raise HTTPException(status_code=404, detail=f"Stock data for {date} not found")

        return {
            "open": float(stock_data["1. open"]),
            "high": float(stock_data["2. high"]),
            "low": float(stock_data["3. low"]),
            "close": float(stock_data["4. close"]),
            "volume": int(stock_data["5. volume"]),
        }

    def determine_output_size_by_date(self, date):
        query_date = self.clean_date(date)
        limit = datetime.datetime.now() - datetime.timedelta(days=20 * 365)
        if query_date < limit:
            logging.info(f"{date} exceeds time scope. Please choose a date within the past 20 years :)")
            raise HTTPException(
                status_code=400,
                detail=f"{date} exceeds time scope."
            )
        if query_date < datetime.datetime.now() - datetime.timedelta(days=100):
            return 'full'
        else:
            return 'compact'

    def clean_date(self, date):
        try:
            return datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

    def get_lowest_low(self, symbol: str, n: int):
        logging.info(f'Getting lowest price for {symbol} from the past {n} days')
        today = datetime.datetime.now().date()
        date = today.strftime("%Y-%m-%d")
        time_series = self.get_stock_data(symbol, date)
        look_back_scope = self.last_n_days_of_time_series(time_series,n)
        lowest_low = min(float(time_series[look_back_date]["3. low"]) for look_back_date in look_back_scope)
        return {"min":lowest_low}

    def get_highest_high(self, symbol: str, n: int):
        logging.info(f'Getting highest price {symbol} from the past {n} days')
        today = datetime.datetime.now().date()
        date = today.strftime("%Y-%m-%d")
        time_series = self.get_stock_data(symbol, date)
        look_back_scope = self.last_n_days_of_time_series(time_series, n)
        highest_high = max(float(time_series[look_back_date]["2. high"]) for look_back_date in look_back_scope)
        return {"max": highest_high}

    def last_n_days_of_time_series(self, data, n):
        time_series_dates = list(data.keys())
        if time_series_dates[0] >= time_series_dates[-1]:
            return time_series_dates[:n]
        return sorted(time_series_dates, reverse=True)[:n]

    def fetch_sample_data(self):
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": "IBM",
            "apikey": "demo",
        }
        response = self.session.get(self.host, params=params)
        return response.json()
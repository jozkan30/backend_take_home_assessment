import requests
import datetime
from fastapi import HTTPException
import logging
from cachetools import cached, TTLCache
from functools import lru_cache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class AlphaVantageAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.host = "https://www.alphavantage.co/query"

    @lru_cache(maxsize=100)
    def get_stock_data(self, symbol: str, outputsize: str):

        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,
            "apikey": self.api_key,
        }

        response = requests.get(self.host, params=params)
        data = response.json()

        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            raise HTTPException(status_code=404, detail="Stock data not found")

        return time_series

    def lookup(self, symbol: str, date: str):
        logging.info(f"Lookup: {symbol} {date}")
        output_size = self.determine_output_size_by_date(date)
        time_series = self.get_stock_data(symbol, output_size)
        stock_data = time_series[date]
        return {
            "open": float(stock_data["1. open"]),
            "high": float(stock_data["2. high"]),
            "low": float(stock_data["3. low"]),
            "close": float(stock_data["4. close"]),
            "volume": int(stock_data["5. volume"]),
        }
    
    def get_lowest_low(self, symbol: str, n: int):
        outputsize = 'full' if n > 100 else 'compact' 
        time_series = self.get_stock_data(symbol, outputsize)
        look_back_scope = self.last_n_days_of_time_series(time_series,n)
        lowest_low = min(float(time_series[date]["3. low"]) for date in look_back_scope)
        return {"min":lowest_low}

    def last_n_days_of_time_series(self, data, n):
        time_series_dates = list(data.keys())
        if time_series_dates[0] >= time_series_dates[-1]:
            return time_series_dates[:n]
        return sorted(time_series_dates, reverse=True)[:n]

    def determine_output_size_by_date(self, date):
        query_date = self.clean_date(date)
        print(query_date)
        limit = datetime.datetime.now() - datetime.timedelta(days=20 * 365)
        if query_date < limit:
            raise HTTPException(
                status_code=400,
                detail=f"{date} exceeds time scope. Please choose a date within the past 20 years :)"
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
    
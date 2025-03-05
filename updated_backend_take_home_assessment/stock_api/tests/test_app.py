import pytest
from unittest.mock import Mock
from src.stock_api.service import AlphaVantageAPI

@pytest.fixture
def alpha_vantage():
    api_key = "TEST_API_KEY"
    return AlphaVantageAPI(api_key)

def test_get_stock_data(alpha_vantage, mocker):
    mock_response = {
        "Time Series (Daily)": {
        "2025-03-04": {
            "1. open": "248.7500",
            "2. high": "255.4800",
            "3. low": "248.1000",
            "4. close": "253.2100",
            "5. volume": "5342106"
        },
        "2025-03-03": {
            "1. open": "254.7350",
            "2. high": "255.9900",
            "3. low": "248.2450",
            "4. close": "250.1900",
            "5. volume": "2977699"
        },
        "2025-02-28": {
            "1. open": "250.8550",
            "2. high": "252.8099",
            "3. low": "246.5400",
            "4. close": "252.4400",
            "5. volume": "7988809"
        }}
    }
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    stock_data = alpha_vantage.get_stock_data("IBM", "2025-02-28")
    stock_data_for_date = stock_data["2025-02-28"]
    assert "2025-02-28" in stock_data
    assert float(stock_data_for_date["1. open"]) == 250.8550
    assert float(stock_data_for_date["2. high"]) == 252.8099

import requests
import curl

url_1 = "http://127.0.0.1:8000/min"
url_2 = "http://127.0.0.1:8000/lookup"
params_1 = {
    "symbol": "IBM",
    "days": 5
}
params_2 = {
    "symbol": "IBM",
    "date": "2025-02-28"
}
headers = {
    "Authorization": ""
}

# lowest = requests.get(url_1, params=params_1, headers=headers)
stock_at_date = requests.get(url_2, params=params_2, headers=headers)
print(stock_at_date.json())
import requests
import curl

host = "http://127.0.0.1:8000"

params_1 = {
    "symbol": "IBM",
    "days": 5
}
params_lookup = {
    "symbol": "IBM",
    "date": "2025-02-28",
}

params_3 = {
    "symbol": "AAPL",
    "days": 5
}

params_4 = {
    "symbol": "F",
    "days": 5
}
headers = {
    "Authorization": "YOUR_API_KEY"
}

lookup_response = requests.get(f"{host}/lookup", params=params_lookup, headers=headers)
lookup_response_again = requests.get(f"{host}/lookup", params=params_lookup, headers=headers)

min_response = requests.get(f"{host}/min", params=params_3, headers=headers)
min_response_again = requests.get(f"{host}/min", params=params_4, headers=headers)

max_response = requests.get(f"{host}/max", params=params_4, headers=headers)

print("\nLookup Response:")
print(lookup_response.status_code)
print(lookup_response.json())
print(curl.parse(lookup_response))

print("\nLookup Response Again:")
print(lookup_response_again.status_code)
print(lookup_response_again.json())

print("\nLowest Low")
print(min_response_again.json())
print(curl.parse(min_response))

print("\nMax:")
print(max_response.json())
print(curl.parse(max_response))
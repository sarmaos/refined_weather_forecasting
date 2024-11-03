#https://www.weather.gov/documentation/services-web-api

import requests
import pandas as pd

api_key = '919ce03b47076ddeed15b96a05e52293'

exclude = 'current, minutely, alerts'
query = '42.3478, -71.0466'
latitude = '42.3478'
longitude = '-71.0466'
url = f'''https://api.weather.gov/points/{latitude},{longitude}'''

response = requests.get(url)
data = response.json()
print(data)
# forecast_hourly_endpoint = data['properties']['forecastHourly']

# h_response = requests.get(forecast_hourly_endpoint)
# print(h_response.json())
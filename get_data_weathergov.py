#https://www.weather.gov/documentation/services-web-api

import requests
import pandas as pd
from utils import normalize_df

def get_weathergov_hourly_forecast(lat, log):
       final_cols = ['startTime', 'endTime', 'isDaytime', 'temperature',
              'temperatureUnit', 'probabilityOfPrecipitation',
              'dewpoint', 'relativeHumidity', 'windSpeed', 'windDirection']

       api_key = '919ce03b47076ddeed15b96a05e52293'

       exclude = 'current, minutely, alerts'
       query = '42.3478, -71.0466'
       # latitude = '42.3478'
       # longitude = '-71.0466'
       url = f'''https://api.weather.gov/points/{lat},{log}'''

       response = requests.get(url)
       data = response.json()
       # print(data)
       forecast_hourly_endpoint = data['properties']['forecastHourly']
       params = {'units':'si'}
       h_response = requests.get(forecast_hourly_endpoint, params=params)
       h_data = h_response.json()['properties']['periods']

       df_hourly = pd.DataFrame(h_data)
       print(df_hourly.columns)
       df_hourly['probabilityOfPrecipitation'] = df_hourly['probabilityOfPrecipitation'].apply(lambda x: x.get('value'))
       df_hourly['relativeHumidity'] = df_hourly['relativeHumidity'].apply(lambda x: x.get('value'))
       df_hourly['dewpoint'] = df_hourly['dewpoint'].apply(lambda x: x.get('value'))

       df_hourly = df_hourly[final_cols]
       return df_hourly

if __name__ == "__main__":
       df_forecast = get_weathergov_hourly_forecast(42.34, -71.04)
       print(df_forecast.head(2))
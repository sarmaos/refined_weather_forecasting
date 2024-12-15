#https://www.weather.gov/documentation/services-web-api

import requests
import pandas as pd
from utils import normalize_df, get_current_ts

def get_weathergov_hourly_forecast(lat, lng):
       final_cols = ['startTime', 'endTime', 'isDaytime', 'temperature',
              'temperatureUnit', 'probabilityOfPrecipitation',
              'dewpoint', 'relativeHumidity', 'windSpeed', 'windDirection']

       api_key = '919ce03b47076ddeed15b96a05e52293'

       exclude = 'current, minutely, alerts'
       query = '42.3478, -71.0466'
       url = f'''https://api.weather.gov/points/{lat},{lng}'''

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
       df_forecast = get_weathergov_hourly_forecast(34.1141, -118.4068)
       df_forecast.to_csv(f'./data/exports/{__file__.split('/')[-1].split('_')[2].split('.')[0]}_export_{get_current_ts()}.csv')
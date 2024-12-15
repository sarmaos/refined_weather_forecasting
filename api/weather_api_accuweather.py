import os
import pandas as pd
import requests
from utils import get_current_ts
from api.weather_api import WeatherAPI
from column_mapper import rename_and_select_columns

class AccuweatherAPI(WeatherAPI):
    def __init__(self, api_key):
        self.api_key = api_key

    def source_name(self):
        return 'accuweather'
        
    def get_raw_data(self, lat: float, lng: float) -> pd.DataFrame:
        params = {'apikey':self.api_key, 'metric':'true', 'details':'true'}
        location = ','.join(str(x) for x in [lat,lng])
        location_params =  {'apikey':self.api_key, 'q':location, 'toplevel':'true'}
        location_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
        location_resp = requests.get(location_url, location_params)
        location_key = location_resp.json()['Key']
        url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}'
        response = requests.get(url, params)
        data = response.json()
        df = pd.DataFrame(data)
        return df
    
    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df['wind_direction'] = df['Wind'].apply(lambda x: x['Direction']['Degrees'])
        df['wind_speed_kmh'] = df['Wind'].apply(lambda x: x['Speed']['Value'])
        df['temperature'] = df['Temperature'].apply(lambda x: x['Value'])
        df['apparent_temperature'] = df['RealFeelTemperature'].apply(lambda x: x['Value'])
        df = rename_and_select_columns(df, self.source_name())
        return df
    


if __name__ == '__main__':
    lat, lng = 34.1141, -118.4068
    accuweather_api = AccuweatherAPI(os.getenv('ACCUWEATHER_APIKEY'))
    df = accuweather_api.get_data(lat, lng)
    print(df.head(5))
    df.to_csv(f'./data/exports/{__file__.split('/')[-1].split('_')[2].split('.')[0]}_export_{get_current_ts()}.csv')
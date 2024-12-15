#https://docs.tomorrow.io/
import os
import requests
import pandas as pd
from utils import get_current_ts
from api.weather_api import WeatherAPI
from column_mapper import rename_and_select_columns

class TomorrowapiAPI(WeatherAPI):
    def __init__(self, api_key):
        self.api_key = api_key

    def source_name(self):
        return 'tomorrowapi'
        
    def get_raw_data(self, lat: float, lng: float) -> pd.DataFrame:
        location = ','.join(str(x) for x in [lat,lng])
        params = {'location':location, 'timesteps':['1d', '1h']}
        url = f'https://api.tomorrow.io/v4/weather/forecast?&apikey={self.api_key}'
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            hourly_data = data['timelines']['hourly']
            df = pd.DataFrame(hourly_data)
            return df
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    
    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        hourly_cols = ['time','cloudCover', 'humidity', 'precipitationProbability', 'temperature', 'temperatureApparent', 'windDirection', 'windGust', 'windSpeed']
        def normalize_df(df, cols):
            values_df = pd.json_normalize(df['values'])
            df = df.drop(columns=['values']).join(values_df)
            return df[cols]
        df = normalize_df(df, hourly_cols)
        df['relative_humidity'] = 0
        df = rename_and_select_columns(df, self.source_name())
        return df
    
    def get_data(self, lat: float, lng: float):
        df = self.get_raw_data(lat, lng)
        normalized_df = self.normalize_data(df)
        return normalized_df
    
if __name__ == '__main__':
    lat, lng = 34.1141, -118.4068
    tomorrowapi_api = TomorrowapiAPI(os.getenv('TOMORROWAPI_APIKEY'))
    df = tomorrowapi_api.get_data(lat, lng)
    print(df.head(5))
    df.to_csv(f'./data/exports/{__file__.split('/')[-1].split('_')[2].split('.')[0]}_export_{get_current_ts()}.csv')

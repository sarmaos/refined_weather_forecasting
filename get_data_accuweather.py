import pandas as pd
import requests
from utils import get_current_ts

def get_accuweather_hourly_forecast(lat: float, lng:float):
    location = ','.join(str(x) for x in [lat,lng])
    api_key = 'cxpveDSpC2InaAQJcnAq7cJaVMcTWuGS'

    params = {'apikey':api_key, 'metric':'true', 'details':'true'}

    location_params =  {'apikey':api_key, 'q':location, 'toplevel':'true'}
    location_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
    location_resp = requests.get(location_url, location_params)
    location_key = location_resp.json()['Key']

    url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}'
    response = requests.get(url, params)
    data = response.json()
    df = pd.DataFrame(data)

    df['wind_direction'] = df['Wind'].apply(lambda x: x['Direction']['Degrees'])
    df['wind_speed_kmh'] = df['Wind'].apply(lambda x: x['Speed']['Value'])
    df['temperature'] = df['Temperature'].apply(lambda x: x['Value'])
    df['apparent_temperature'] = df['RealFeelTemperature'].apply(lambda x: x['Value'])
    return df

if __name__ == '__main__':
    df_forecast = get_accuweather_hourly_forecast(34.1141, -118.4068)
    df_forecast.to_csv(f'./data/exports/{__file__.split('/')[-1].split('_')[2].split('.')[0]}_export_{get_current_ts()}.csv')
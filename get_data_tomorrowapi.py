#https://docs.tomorrow.io/

import requests
import pandas as pd
from utils import get_current_ts
import numpy as np
def get_tomorrowapi_hourly_forecast(lat, lng):

    location = ','.join(str(x) for x in [lat,lng])

    api_key = 'dv4p5Wt3NImiYihzPHSF0Dz1CiDb1uok'

    city_name = ''

    url = f'https://api.tomorrow.io/v4/weather/forecast?&apikey={api_key}'

    hourly_cols = ['time','cloudCover', 'humidity', 'precipitationProbability', 'temperature', 'temperatureApparent', 'windDirection', 'windGust', 'windSpeed']

    # params = {'location':'42.3478,-71.0466', 'timesteps':['1d', '1h']}
    params = {'location':location, 'timesteps':['1d', '1h']}

    response = requests.get(url, params=params)

    data = response.json()

    hourly_data = data['timelines']['hourly']

    def normalize_df(df, cols):
        values_df = pd.json_normalize(df['values'])
        df = df.drop(columns=['values']).join(values_df)
        return df[cols]

    df_hourly = pd.DataFrame(hourly_data)
    df_hourly = normalize_df(df_hourly, hourly_cols)
    df_hourly['relative_humidity'] = 0
    return df_hourly

if __name__ == "__main__":
    df_forecast = get_tomorrowapi_hourly_forecast(34.1141, -118.4068)
    df_forecast.to_csv(f'./data/exports/{__file__.split('/')[-1].split('_')[2].split('.')[0]}_export_{get_current_ts()}.csv')

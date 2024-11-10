#https://docs.tomorrow.io/

import requests
import pandas as pd

def get_weathergov_hourly_forecast(lat, log):

    location = ','.join(str(x) for x in [lat,log])

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
    return df_hourly

if __name__ == "__main__":
    df_forecast = get_weathergov_hourly_forecast(42.34, -71.04)
    print(df_forecast.head(2))


#https://docs.tomorrow.io/

import requests
import pandas as pd

api_key = 'dv4p5Wt3NImiYihzPHSF0Dz1CiDb1uok'

city_name = ''

url = f'https://api.tomorrow.io/v4/weather/forecast?&apikey={api_key}'

hourly_cols = ['time','cloudCover', 'humidity', 'precipitationProbability', 'temperature', 'temperatureApparent', 'windDirection', 'windGust', 'windSpeed']
daily_cols = ['time','cloudCoverAvg', 'humidityAvg', 'precipitationProbabilityAvg', 'temperatureAvg', 'temperatureApparentAvg', 'windDirectionAvg', 'windGustAvg', 'windSpeedAvg']
# params = {'location':'42.3478,-71.0466', 'timesteps':['1d', '1h']}
params = {'location':'42.3478,-71.0466', 'timesteps':['1d', '1h']}
# 
response = requests.get(url, params=params)

data = response.json()
# print(data)

# hourly_data = response.timelines
daily_data = data['timelines']['daily']
hourly_data = data['timelines']['hourly']

def normalize_df(df, cols):
    values_df = pd.json_normalize(df['values'])
    df = df.drop(columns=['values']).join(values_df)
    return df[cols]

df_daily = pd.DataFrame(daily_data)
df_daily = normalize_df(df_daily, daily_cols)

df_hourly = pd.DataFrame(hourly_data)
df_hourly = normalize_df(df_hourly, hourly_cols)

print(df_daily.head())
print(df_hourly.head())
# df_daily.to_csv('./data/daily_data_sample.csv')
# df2 = pd.DataFrame(hourly_data)
# print(dftmp.head())


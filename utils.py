import pandas as pd
import datetime

def get_current_ts():
    return str(datetime.datetime.now()).replace(' ','').replace(':','').replace('.','')


def normalize_df(df, cols, normalize_col):
    values_df = pd.json_normalize(df[normalize_col])
    df = df.drop(columns=[normalize_col]).join(values_df)
    return df[cols]

def get_coordinates(city: str, country: str):
    city_data = pd.read_csv('./data/worldcities.csv')
    filtered_data = city_data[(city_data['city']==city)&(city_data['country']==country)]
    lat = filtered_data.lat.values[0]
    lng = filtered_data.lng.values[0]
    if filtered_data.shape[0]>0:
        print(f'Coordinates {lat}/{lng} for city {city} found.')
    return lat, lng

def normalize_city_param(source):
    pass
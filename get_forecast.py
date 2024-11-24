import pandas as pd
from get_data_openmeteo import get_openmeteo_hourly_forecast
from get_data_tomorrowapi import get_tomorrowapi_hourly_forecast
from get_data_weathergov import get_weathergov_hourly_forecast
from get_data_accuweather import get_accuweather_hourly_forecast
from utils import get_coordinates
from column_mapper import rename_and_select_columns


def get_hourly_forecast_with_coordinates(lat: float, lng: float, src: str) -> pd.DataFrame:
    if src == 'openmeteo':
        return get_openmeteo_hourly_forecast(lat, lng)
    elif src == 'tomorrowapi':
        return get_tomorrowapi_hourly_forecast(lat, lng)
    elif src == 'weathergov':
        return get_weathergov_hourly_forecast(lat, lng)
    elif src == 'accuweather':
        return get_accuweather_hourly_forecast(lat, lng)
    else:
        raise Exception(f'src parameter "{src}" is not valid.')
    pass

def combine_forecasts(lat, lng):
    df_master = pd.DataFrame()
    srcs = ['openmeteo','tomorrowapi','accuweather']
    for src in srcs:
        try:
            forecast_df = get_hourly_forecast_with_coordinates(lat, lng, src)
            forecast_df = rename_and_select_columns(forecast_df, src)
            forecast_df['source'] = src
            df_master = pd.concat([df_master, forecast_df])
        except Exception as e:
            print(f'There was an error with {src}')
            print(e)
            continue
    return df_master
        

def get_hourly_forecast(city: str, country: str) -> pd.DataFrame:
    lat,lng = get_coordinates(city, country)
    forecast_df = combine_forecasts(lat, lng)
    cols = [col for col in forecast_df.columns if col  not in ['source', 'time']]
    ensemble_df = forecast_df.groupby('time')[cols].mean().reset_index()
    ensemble_df['source'] = 'ensemble'
    final_df = pd.concat([forecast_df, ensemble_df], ignore_index=True)
    return final_df
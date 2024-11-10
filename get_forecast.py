import pandas as pd

def get_coordinates(city):
    city_data = pd.read_csv('./data/worldcities.csv')
    filtered_data = city_data[city_data['city']==city]
    lat = filtered_data.lat[0]
    log = filtered_data.lat[0]
    return lat, log

def get_hourly_forecast_with_coordinates(lat, log, src):
    if src == 'openmeteo':
        
    pass


def get_hourly_forecast(city: str, src: str) -> pd.DataFrame:
    lat,log = get_coordinates(city)
    forecast = get_hourly_forecast_with_coordinates(lat, log, src)
    pass
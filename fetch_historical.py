from api.weather_api_openmeteo import OpenmeteoAPI
from api.weather_api_tomorrowapi import TomorrowapiAPI
from utils import get_current_ts
import os

def main(source):
    lat, lng = 37.9842, 23.7281
    if source == 'openmeteo':
        openmeteo_api = OpenmeteoAPI()
        df = openmeteo_api.get_historical_data(lat, lng)
    elif source == 'tomorrowapi':
        tomorrowapi_api = TomorrowapiAPI(api_key=os.getenv('TOMORROWAPI_APIKEY'))
        df = tomorrowapi_api.get_historical_data(lat, lng)
    print(df.head(5))
    df.to_csv(f'./local_data/exports/HISTORICAL_export_{get_current_ts()}.csv')


if __name__ == "__main__":
    main(source = 'openmeteo')
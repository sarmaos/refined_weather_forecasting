from api.weather_api_openmeteo import OpenmeteoAPI
from utils import get_current_ts

def main():
    lat, lng = 37.9842, 23.7281
    openmeteo_api = OpenmeteoAPI()
    df = openmeteo_api.get_historical_data(lat, lng)
    print(df.head(5))
    df.to_csv(f'./local_data/exports/HISTORICAL_export_{get_current_ts()}.csv')


if __name__ == "__main__":
    main()
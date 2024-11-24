from get_forecast import get_hourly_forecast
from utils import get_current_ts

if __name__ == "__main__":
    df_forecast = get_hourly_forecast(city = 'Athens', country = 'Greece')
    print(df_forecast.head(5))
    df_forecast.to_csv(f'./data/exports/combined/combined_{get_current_ts()}.csv')
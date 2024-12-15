from utils import get_coordinates
from api.weather_api_tomorrowapi import TomorrowapiAPI
from api.weather_api_accuweather import AccuweatherAPI
from api.weather_api_openmeteo import OpenmeteoAPI
from model.weather_ensemble import EnsembleFactory
from utils import get_current_ts
import os

def get_hourly_forecast(city, country, ensemble_strategy = "simple_average"):

    lat, lng = get_coordinates(city, country)
        
    tomorrow_api = TomorrowapiAPI(os.getenv('TOMORROWAPI_APIKEY'))
    accuweather = AccuweatherAPI(os.getenv('ACCUWEATHER_APIKEY'))
    open_meteo = OpenmeteoAPI()

    tomorrow_data = tomorrow_api.get_data(lat, lng)
    open_meteo_data = open_meteo.get_data(lat, lng)
    accuweather_data = accuweather.get_data(lat, lng)

    ensemble_strategy = EnsembleFactory.get_ensemble_strategy(ensemble_strategy)
    data = ensemble_strategy.generate_ensemble([tomorrow_data, open_meteo_data, accuweather_data])
    return data


if __name__ == "__main__":
    strategy = 'simple_average'
    data = get_hourly_forecast('Athens','Greece',strategy)
    data.to_csv(f'./local_data/exports/ENSEMBLE_{strategy}_{get_current_ts()}.csv')
#https://open-meteo.com/

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def get_openmeteo_hourly_forecast(lat, log):
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		# "latitude": 52.52,
		# "longitude": 13.41,
		"latitude": lat,
		"longitude": log,
		"hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "cloud_cover", "wind_speed_120m", "wind_direction_120m", "wind_gusts_10m", "temperature_120m"]
	}
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]

	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()
	hourly_cloud_cover = hourly.Variables(4).ValuesAsNumpy()
	hourly_wind_speed_120m = hourly.Variables(5).ValuesAsNumpy()
	hourly_wind_direction_120m = hourly.Variables(6).ValuesAsNumpy()
	hourly_wind_gusts_10m = hourly.Variables(7).ValuesAsNumpy()
	hourly_temperature_120m = hourly.Variables(8).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["apparent_temperature"] = hourly_apparent_temperature
	hourly_data["precipitation_probability"] = hourly_precipitation_probability
	hourly_data["cloud_cover"] = hourly_cloud_cover
	hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
	hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
	hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
	hourly_data["temperature_120m"] = hourly_temperature_120m

	hourly_dataframe = pd.DataFrame(data = hourly_data)
	return hourly_dataframe


if __name__ == "__main__":
	df_forecast = get_openmeteo_hourly_forecast(52.52, 13.41)
	print(df_forecast.head(2))
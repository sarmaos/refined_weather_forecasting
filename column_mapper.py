import pandas as pd

column_mapping = {
    'tomorrowapi': {
        'time': 'time',
        'temperatureApparent': 'feels_like',
        'humidity': 'relative_humidity',
        'precipitationProbability': 'precipitation_probability',
        'temperature': 'temperature_c',
        'windDirection': 'wind_direction',
        'windSpeed': 'wind_speed'
    },
    'openmeteo': {
        'date': 'time',
        'apparent_temperature': 'feels_like',
        'relative_humidity_2m': 'relative_humidity',
        'precipitation_probability': 'precipitation_probability',
        'temperature_2m': 'temperature_c',
        'wind_direction_120m': 'wind_direction',
        'wind_speed_120m': 'wind_speed'
    },
    'weathergov': {
        'startTime': 'time',
        'relativeHumidity': 'relative_humidity',
        'probabilityOfPrecipitation': 'precipitation_probability',
        'temperature': 'temperature_c',
        'windDirection': 'wind_direction',
        'windSpeed': 'wind_speed'
    },
    'accuweather': {
        'DateTime': 'time',
        'apparent_temperature': 'feels_like',
        'RelativeHumidity': 'relative_humidity',
        'PrecipitationProbability': 'precipitation_probability',
        'temperature': 'temperature_c',
        'wind_direction': 'wind_direction',
        'wind_speed_kmh': 'wind_speed'
    }
}

def apply_dtypes(df):
    dtype_mapping = {
        'time': 'datetime64[ns, UTC]',    # Ensure time is a datetime object
        'feels_like': 'float64',     # Feels like should be a float with 2 decimals
        'relative_humidity': 'int64',  # Relative humidity should be an integer (1-100)
        'precipitation_probability': 'int64',  # Precipitation probability should be an integer (1-100)
        'temperature_c': 'float64',   # Temperature in Celsius should be a float with 2 decimals
        'wind_direction': 'int64',    # Wind direction in degrees (integer)
        'wind_speed': 'float64'       # Wind speed should be a float with 2 decimals
    }
    for col in df.columns:
        dtype = dtype_mapping[col]
        # if dtype == 'datetime64[ns]' and pd.api.types.is_datetime64_any_dtype(df[col]):
        #     if df[col].dt.tz is not None:
        #         df[col] = df[col].dt.tz_localize(None)
        df[col] = df[col].astype(dtype)
        if dtype == 'float64':
            df[col] = df[col].round(2)
    return df
   
def rename_and_select_columns(df: pd.DataFrame, source: str) -> pd.DataFrame:
    if source not in column_mapping:
        raise ValueError(f"Unknown data source: {source}")
    column_rename = column_mapping[source]
    df_renamed = df.rename(columns=column_rename)
    desired_columns = ['time', 'feels_like', 'relative_humidity', 
                       'precipitation_probability', 'temperature_c', 
                       'wind_direction', 'wind_speed']
    df_renamed = df_renamed[desired_columns]
    df_renamed = apply_dtypes(df_renamed)
    df_renamed['source'] = source
    return df_renamed

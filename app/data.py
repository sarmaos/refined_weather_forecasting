import pandas as pd
from api.api import get_hourly_forecast
import streamlit as st

@st.cache_data
def load_city_data(file_path):
    return pd.read_csv(file_path)


def fetch_weather_data(city, country, strategy, use_dummy_data=False):
    if use_dummy_data:
        # Load dummy data for testing
        return pd.read_csv("data/dummy_weather_data.csv", parse_dates=["time"])
    else:
        # Original API call logic
        return get_hourly_forecast(city, country, strategy)
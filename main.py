import streamlit as st
from app.data import load_city_data, fetch_weather_data
from app.auth import setup_authenticator
from app.display import display_hour_metrics, display_footer
import pandas as pd
from app.plots import (
    plot_hourly_data,
    plot_precipitation_bar,
    plot_average_wind_speed_gauge,
    plot_data_table,
)

@st.cache_data
def load_hourly_data(city, country, selected_strategy):
    return fetch_weather_data(city, country, selected_strategy)

def main():
    st.title("Weather Forecast App 🌦️")
    st.markdown("Get hourly weather forecasts for your city, sourced from multiple data providers.")

    # Sidebar configuration
    st.sidebar.header("Configuration")
    file_path = "data/worldcities.csv"
    cities_data = load_city_data(file_path)

    # Ensemble strategy selection
    ensemble_strategies = ["", "simple_average", "weighted_average"]
    selected_strategy = st.sidebar.selectbox(
        "Select Ensemble Strategy", 
        ensemble_strategies, 
        index=2,  # Default to "weighted_average"
        format_func=lambda x: "Select..." if x == "" else x, 
        key='select_strategy',
    )

    # Country and city selection
    countries = sorted(cities_data["country"].unique())
    country = st.sidebar.selectbox(
        "Select Country", [""] + countries, index=0,
        format_func=lambda x: "Select..." if x == "" else x,key='select_country'
    )
    city = None
    if country:
        filtered_cities = sorted(cities_data[cities_data["country"] == country]["city"].unique())
        city = st.sidebar.selectbox(
            "Select City", [""] + filtered_cities, index=0,
            format_func=lambda x: "Select..." if x == "" else x, key='select_city'
        )

    # Display weather data
    if city and country and selected_strategy:
        st.write(f"### {city}, {country} 12-hour forecast")

        # Fetch weather data
        with st.spinner("Fetching weather data..."):
            hourly_data = load_hourly_data(city, country, selected_strategy)

        if not hourly_data.empty:
            hourly_data["time"] = pd.to_datetime(hourly_data["time"])

            ensemble_hourly = hourly_data[hourly_data.source=='ensemble']
            

            # selected_hour = st.slider(
            #         "Select Forecast Hour", 0, len(ensemble_hourly) - 1, 1, format="Hour %d"
            #     )
            selected_data = ensemble_hourly.iloc[1]

            # Display metrics for selected hour
            display_hour_metrics(selected_data)

            metrics = [
                    "temperature_c", "feels_like", "relative_humidity",
                    "precipitation_probability", "wind_speed", "wind_direction"
                ]
            selected_metric = st.selectbox("Metric", metrics, index=0)
            plot_hourly_data(hourly_data, selected_metric)

            col1, col2 = st.columns([2, 1])

            with col1:
                plot_precipitation_bar(ensemble_hourly)

            with col2:
                plot_average_wind_speed_gauge(ensemble_hourly)

            plot_data_table(hourly_data)
                
        else:
            st.error("No weather data available for the selected location.")
    else:
        st.info("Please select a country, city, and ensemble strategy from the sidebar.")

    # Footer
    display_footer()
    
if __name__ == "__main__":
    # Setup authenticator
    authenticator = setup_authenticator('./config.yaml')

    if st.session_state.get("authentication_status"):
        authenticator.logout()
        st.write(   f"Welcome *{st.session_state['name']}*")
        main()
    elif st.session_state.get("authentication_status") is False:
        st.error("Username/password is incorrect")
    else:
        st.warning("Please enter your username and password")
        st.markdown("For acquiring access to the specific application send an email to sarmaos@athtech.gr")
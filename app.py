import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from main import get_hourly_forecast

# Load cities data from CSV file
@st.cache_data
def load_city_data(file_path):
    return pd.read_csv(file_path)

# Fetch weather data
def fetch_weather_data(city, country, strategy):
    return get_hourly_forecast(city, country, strategy)

# Setup and authenticate user
def setup_authenticator(config_path):
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    return authenticator

# Display weather metrics for the next hour
def display_next_hour_metrics(next_hour_data):
    st.subheader("Next Hour's Forecast")
    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", f"{next_hour_data['temperature_c']:.2f}" if next_hour_data is not None else "N/A")
        col2.metric("Feels Like (°C)", f"{next_hour_data['feels_like']:.2f}" if next_hour_data is not None else "N/A")
        col3.metric("Precipitation (%)", f"{next_hour_data['precipitation_probability']}%" if next_hour_data is not None else "N/A")

    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("Wind Speed (km/h)", f"{next_hour_data['wind_speed']:.2f}" if next_hour_data is not None else "N/A")
        col2.metric("Wind Direction (°)", f"{next_hour_data['wind_direction']}" if next_hour_data is not None else "N/A")
        col3.metric("Relative Humidity (%)", f"{next_hour_data['relative_humidity']}%" if next_hour_data is not None else "N/A")

# Plot hourly data
def plot_hourly_data(hourly_data, selected_metric):
    fig = px.line(
        hourly_data, x="time", y=selected_metric, color="source",
        title=f"Hourly {selected_metric.replace('_', ' ').capitalize()} Forecast",
        labels={
            selected_metric: selected_metric.replace('_', ' ').capitalize(),
            "time": "Time"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# Main app
def main():
    st.title("Weather Forecast App 🌦️")
    st.markdown("Get hourly weather forecasts for your city, sourced from multiple data providers.")

    # Sidebar configuration
    st.sidebar.header("Configuration")
    file_path = "data/worldcities.csv"
    cities_data = load_city_data(file_path)

    # Ensemble strategy selection
    ensemble_strategies = ["", "simple_average", "weighted_average", "median"]
    selected_strategy = st.sidebar.selectbox(
        "Select Ensemble Strategy", ensemble_strategies, index=0,
        format_func=lambda x: "Select..." if x == "" else x
    )

    # Country and city selection
    countries = sorted(cities_data["country"].unique())
    country = st.sidebar.selectbox(
        "Select Country", [""] + countries, index=0,
        format_func=lambda x: "Select..." if x == "" else x
    )
    city = None
    if country:
        filtered_cities = sorted(cities_data[cities_data["country"] == country]["city"].unique())
        city = st.sidebar.selectbox(
            "Select City", [""] + filtered_cities, index=0,
            format_func=lambda x: "Select..." if x == "" else x
        )

    # Display weather data
    if city and country and selected_strategy:
        st.write(f"### Weather Data for {city}, {country} (Strategy: {selected_strategy})")

        # Fetch weather data
        with st.spinner("Fetching weather data..."):
            hourly_data = fetch_weather_data(city, country, selected_strategy)

        if not hourly_data.empty:
            hourly_data["time"] = pd.to_datetime(hourly_data["time"])

            # Next hour's data
            next_hour_data = hourly_data.iloc[1] if len(hourly_data) > 1 else None
            display_next_hour_metrics(next_hour_data)

            # Metric selection
            st.subheader("Select Metric to Display")
            metrics = [
                "temperature_c", "feels_like", "relative_humidity",
                "precipitation_probability", "wind_speed", "wind_direction"
            ]
            selected_metric = st.selectbox("Metric", metrics, index=0)

            # Plot data
            plot_hourly_data(hourly_data, selected_metric)
        else:
            st.error("No weather data available for the selected location.")
    else:
        st.info("Please select a country, city, and ensemble strategy from the sidebar.")

    # Footer
    st.markdown("---")
    st.markdown(
        "Created by **Spyros Armaos** for educational purposes. 🌍\n\n"
        "This app demonstrates how multiple weather forecasting services can be combined in a single application to get better forecasts."
    )

if __name__ == "__main__":
    # Setup authenticator
    authenticator = setup_authenticator('./config.yaml')

    if st.session_state.get("authentication_status"):
        authenticator.logout()
        st.write(f"Welcome *{st.session_state['name']}*")
        main()
    elif st.session_state.get("authentication_status") is False:
        st.error("Username/password is incorrect")
    else:
        st.warning("Please enter your username and password")
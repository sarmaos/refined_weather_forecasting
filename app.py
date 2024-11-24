import streamlit as st
import pandas as pd
import plotly.express as px
from time import sleep  # Simulate delay for demonstration purposes
from get_forecast import get_hourly_forecast

# Placeholder function to simulate fetching weather data (to be replaced with real implementation)
def fetch_weather_data(city, country):
    return get_hourly_forecast(city, country)

# Load cities data from CSV file
@st.cache_data
def load_city_data(file_path):
    return pd.read_csv(file_path)

# Streamlit app
def main():
    st.title("Weather Forecast App 🌦️")
    st.markdown("Get hourly weather forecasts for your city, sourced from multiple data providers.")

    # Sidebar for city selection
    st.sidebar.header("Location Selection")
    file_path = "data/worldcities.csv"
    cities_data = load_city_data(file_path)
    
    country = st.sidebar.selectbox("Select Country", sorted(cities_data["country"].unique()))
    city = None
    if country:
        filtered_cities = cities_data[cities_data["country"] == country]["city"].unique()
        city = st.sidebar.selectbox("Select City", sorted(filtered_cities))

    # Main content area
    if city and country:
        st.write(f"### Weather Data for {city}, {country}")

        # Fetch weather data with a loading spinner
        with st.spinner("Fetching weather data..."):
            hourly_data = fetch_weather_data(city, country)

        if not hourly_data.empty:
            # Convert time column to datetime
            hourly_data["time"] = pd.to_datetime(hourly_data["time"])

            # Extract the next hour's forecast
            next_hour_data = hourly_data.iloc[1] if len(hourly_data) > 1 else None

            # Display cards for next hour's forecast
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

            # Select metric to display
            st.subheader("Select Metric to Display")
            metrics = ["temperature_c", "feels_like", "relative_humidity",
                       "precipitation_probability", "wind_speed", "wind_direction"]
            selected_metric = st.selectbox("Metric", metrics, index=0)

            # Plot hourly data
            fig_hourly = px.line(hourly_data, x="time", y=selected_metric, color="source",
                                 title=f"Hourly {selected_metric.replace('_', ' ').capitalize()} Forecast",
                                 labels={selected_metric: selected_metric.replace('_', ' ').capitalize(), "time": "Time"})
            st.plotly_chart(fig_hourly, use_container_width=True)
        else:
            st.error("No weather data available for the selected location.")
    else:
        st.info("Please select a country and city from the sidebar.")

    st.markdown("---")
    st.markdown(
            "Created by **Spyros Armaos** for educational purposes. 🌍\n\n"
            "This app demonstrates the use of how multiple weather forecasting services can be combined in a single application to get better forecasts."
        )

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Placeholder function to simulate fetching weather data (to be replaced by actual API call)
def fetch_weather_data(city):
    # This function should return a dictionary containing the weather data.
    # Example format:
    # {
    #     "hourly": {"time": [...], "temperature": [...], "precipitation": [...], "wind_speed": [...]},
    #     "daily": {"date": [...], "temperature": [...], "precipitation": [...], "wind_speed": [...]}
    # }
    return {
        "hourly": {
            "time": ["00:00", "01:00", "02:00", "03:00"],
            "temperature": [15, 14, 13, 13],
            "precipitation": [0, 0.1, 0.3, 0.0],
            "wind_speed": [5, 4, 6, 5]
        },
        "daily": {
            "date": ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04"],
            "temperature": [16, 17, 15, 14],
            "precipitation": [0.5, 0.0, 0.2, 0.1],
            "wind_speed": [4, 5, 6, 5]
        }
    }

# Streamlit app
def main():
    st.title("Weather Forecast App")
    st.write("Get hourly and daily weather forecasts for your city.")

    # Input field for city
    city = st.text_input("Enter the city name", "")

    if city:
        st.write(f"Fetching weather data for: {city}")

        # Fetch weather data
        data = fetch_weather_data(city)

        if data:
            # Hourly forecast
            st.subheader("Hourly Forecast")
            hourly_data = pd.DataFrame(data["hourly"])
            st.write(hourly_data)

            # Plotting hourly data
            fig, ax = plt.subplots()
            ax.plot(hourly_data["time"], hourly_data["temperature"], label="Temperature (°C)")
            ax.plot(hourly_data["time"], hourly_data["precipitation"], label="Precipitation (mm)")
            ax.plot(hourly_data["time"], hourly_data["wind_speed"], label="Wind Speed (km/h)")
            ax.set_xlabel("Time")
            ax.set_title("Hourly Forecast")
            ax.legend()
            st.pyplot(fig)

            # Daily forecast
            st.subheader("Daily Forecast")
            daily_data = pd.DataFrame(data["daily"])
            st.write(daily_data)

            # Plotting daily data
            fig, ax = plt.subplots()
            ax.plot(daily_data["date"], daily_data["temperature"], label="Temperature (°C)")
            ax.plot(daily_data["date"], daily_data["precipitation"], label="Precipitation (mm)")
            ax.plot(daily_data["date"], daily_data["wind_speed"], label="Wind Speed (km/h)")
            ax.set_xlabel("Date")
            ax.set_title("Daily Forecast")
            ax.legend()
            st.pyplot(fig)
        else:
            st.error("Could not fetch weather data. Please try again later.")

if __name__ == "__main__":
    main()

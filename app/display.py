import streamlit as st


def display_hour_metrics(hour_data):
    st.subheader("Next hour's forecast")
    with st.container(border=True):
        with st.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature (°C)", f"{hour_data['temperature_c']:.0f}")
            col2.metric("Feels Like (°C)", f"{hour_data['feels_like']:.0f}")
            col3.metric("Precipitation (%)", f"{hour_data['precipitation_probability']:.0f}%")

        with st.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Wind Speed (km/h)", f"{hour_data['wind_speed']:.0f}")
            col2.metric("Wind Direction (°)", f"{hour_data['wind_direction']:.0f}")
            col3.metric("Relative Humidity (%)", f"{hour_data['relative_humidity']:.0f}%")


def display_footer():
    st.markdown("---")
    st.markdown(
        "Created by **Spyros Armaos** for educational purposes. 🌍\n\n"
        "This app uses OpenMeteo, AccuWeather & Tomorrowio APIs to demonstrate how multiple weather forecasting services can be combined in a single application to get a more precise forecast."
    )

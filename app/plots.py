import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


def plot_hourly_data(hourly_data, selected_metric):
    fig = px.line(
        hourly_data,
        x="time",
        y=selected_metric,
        color="source",
        title=f"Hourly {selected_metric.replace('_', ' ').capitalize()} Forecast",
        labels={"time": "Time"}
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_precipitation_bar(hourly_data):
    fig = px.bar(
        hourly_data,
        x="time",
        y="precipitation_probability",
        color="source",
        title="Precipitation Probability (%)",
        labels={"time": "Time", "precipitation_probability": "Precipitation (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_average_wind_speed_gauge(hourly_data):
    # Calculate the average wind speed across all sources
    avg_speed = hourly_data["wind_speed"].mean()

    # Create the gauge chart
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_speed,
            title={"text": "Average Wind Speed (km/h)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 25], "color": "lightgreen"},
                    {"range": [25, 50], "color": "yellow"},
                    {"range": [50, 75], "color": "orange"},
                    {"range": [75, 100], "color": "red"}
                ],
            },
        )
    )
    st.plotly_chart(fig, use_container_width=True)

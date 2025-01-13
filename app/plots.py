import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

def plot_hourly_data(hourly_data, selected_metric):
    fig = px.line(
        hourly_data,
        x="time",
        y=selected_metric,
        color="source",
        title=f"Hourly {selected_metric.replace('_', ' ').capitalize()} Forecast",
        labels={"time": "Time"}
    )

    for trace in fig.data:
        if trace.name != "ensemble":  # Set opacity for non-ensemble traces
            trace.update(opacity=0.3)
        else:  # Add markers and labels for the "ensemble" trace
            trace.update(
                mode="lines+markers+text",  # Show line, markers, and text labels
                marker=dict(size=8),  # Adjust marker size if needed
                text=[f"{y:.0f}" for y in trace.y],  # Format labels to 2 decimals
                textposition="top center",  # Position labels above the points
                texttemplate="%{text}"  # Display the text as is
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
    # Create wind strength bins
    bins_speed = [0, 10, 20, 30, 40, 50, np.inf]
    labels_speed = ["0-10", "10-20", "20-30", "30-40", "40-50", "50+"]
    hourly_data['strength'] = pd.cut(hourly_data['wind_speed'], bins=bins_speed, labels=labels_speed, right=False)
    
    # Map degrees to directions
    def degrees_to_direction(deg):
        compass = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                   'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        idx = int((deg % 360) / 22.5)  # Divide into 16 segments
        return compass[idx]

    hourly_data['direction'] = hourly_data['wind_direction'].apply(degrees_to_direction)

    # Ensure directions are ordered
    direction_order = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                       'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    hourly_data['direction'] = pd.Categorical(hourly_data['direction'], categories=direction_order, ordered=True)

    # Group by direction and strength to calculate frequency
    df_summary = hourly_data.groupby(['direction', 'strength']).size().reset_index(name='frequency')

    # Plot polar bar chart
    fig = px.bar_polar(
        df_summary,
        r="frequency",
        theta="direction",
        color="strength",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        start_angle=90  # Rotate chart to place NORTH at the top
    )

    # Adjust legend position
    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Adjust vertical position
            x=0.5,  # Center the legend
            xanchor="center",
            yanchor="top"
        )
    )

    # Display chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    
# def plot_average_wind_speed_gauge(hourly_data):
#     # Calculate the average wind speed across all sources
#     avg_speed = hourly_data["wind_speed"].mean()

#     # Create the gauge chart
#     fig = go.Figure(
#         go.Indicator(
#             mode="gauge+number",
#             value=avg_speed,
#             title={"text": "Average Wind Speed (km/h)"},
#             gauge={
#                 "axis": {"range": [0, 100]},
#                 "bar": {"color": "darkblue"},
#                 "steps": [
#                     {"range": [0, 25], "color": "lightgreen"},
#                     {"range": [25, 50], "color": "yellow"},
#                     {"range": [50, 75], "color": "orange"},
#                     {"range": [75, 100], "color": "red"}
#                 ],
#             },
#         )
#     )
#     st.plotly_chart(fig, use_container_width=True)

def plot_data_table(hourly_data):
   st.markdown('### Ensemble data table')
   filtered_hourly_data = hourly_data[hourly_data['source']=='ensemble']
   filtered_hourly_data = filtered_hourly_data[[col for col in filtered_hourly_data if col != 'weight']]
   st.dataframe(filtered_hourly_data, use_container_width=True)

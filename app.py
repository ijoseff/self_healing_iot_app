import streamlit as st
import json
from azure.iot.device import IoTHubDeviceClient
import random
import time
import pandas as pd
import plotly.graph_objects as go
import openai  # Import OpenAI for GPT API
import os

# Retrieve the OpenAI API key from environment variables
openai.api_key = "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"

# Replace with your Azure IoT Hub connection string
IOT_HUB_CONNECTION_STRING = "HostName=simply-automate.azure-devices.net;DeviceId=simulated-device;SharedAccessKey=8gX1+FD9a0nOkXlinPZq1JvHYTEqmZqHpMvvMOUS6YU="

# Global DataFrame to store telemetry data
if 'data_history' not in st.session_state:
    st.session_state.data_history = pd.DataFrame(columns=["timestamp", "heart_rate", "steps"])

def get_device_data():
    heart_rate = random.randint(60, 100)
    steps = random.randint(0, 10000)

    # Create a client instance
    client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONNECTION_STRING)

    # Create a JSON payload
    payload = {
        "heart_rate": heart_rate,
        "steps": steps,
        "timestamp": time.time()
    }

    # Send the telemetry data to the IoT Hub
    client.send_message(json.dumps(payload))
    client.shutdown()  # Close the connection

    return payload

# Function to plot the data with dual-axis
def plot_data():
    if not st.session_state.data_history.empty:
        fig = go.Figure()

        # Add heart rate trace
        fig.add_trace(go.Scatter(
            x=st.session_state.data_history['timestamp'],
            y=st.session_state.data_history['heart_rate'],
            name='Heart Rate (bpm)',
            yaxis='y1',
            mode='lines+markers',
            marker=dict(color='blue')
        ))

        # Add steps trace
        fig.add_trace(go.Scatter(
            x=st.session_state.data_history['timestamp'],
            y=st.session_state.data_history['steps'],
            name='Steps',
            yaxis='y2',
            mode='lines+markers',
            marker=dict(color='orange')
        ))

        # Update layout for dual axes
        fig.update_layout(
            title='Health Monitoring Data',
            xaxis=dict(title='Timestamp'),
            yaxis=dict(title='Heart Rate (bpm)', side='left', showgrid=False),
            yaxis2=dict(title='Steps', side='right', overlaying='y', showgrid=False),
            legend=dict(x=0.1, y=0.9),
            template='plotly_white'
        )

        st.plotly_chart(fig)

def get_gpt_insights(avg_heart_rate, avg_steps):
    messages = [
        {"role": "system", "content": "You are a helpful assistant providing health insights based on user data."},
        {"role": "user", "content": f"Based on an average heart rate of {avg_heart_rate:.2f} bpm and average daily steps of {avg_steps:.2f}, provide a brief insight on health, a recommendation for improvement, and a motivational message."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=messages,
        max_tokens=100,
        temperature=0.7,
    )

    insights = response['choices'][0]['message']['content'].strip()
    return insights

st.set_page_config(page_title="Health Monitoring Dashboard", layout="wide")
st.title("🏥 Real-Time Health Monitoring Dashboard")
st.sidebar.header("Settings")
refresh_interval = st.sidebar.slider("Data Refresh Interval (seconds)", min_value=1, max_value=10, value=5)

# Show that the data is pulling from the IoT cloud
st.markdown("### Data is being retrieved from Azure IoT Hub...")

# Simulated data display
if st.button('Get Latest Data'):
    with st.spinner('Fetching data from IoT Hub...'):
        data = get_device_data()
        new_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['timestamp'])),
            "heart_rate": data['heart_rate'],
            "steps": data['steps']
        }
        
        # Convert new_data to DataFrame
        new_data_df = pd.DataFrame([new_data])
        
        # Use pd.concat to append the new data
        st.session_state.data_history = pd.concat([st.session_state.data_history, new_data_df], ignore_index=True)

        st.success("Data retrieved successfully!")
        st.write(f"**Heart Rate:** {data['heart_rate']} bpm")
        st.write(f"**Steps:** {data['steps']} steps")
        st.write(f"**Timestamp:** {new_data['timestamp']}")

# Plot historical data
st.subheader("Historical Data")
plot_data()

# Add additional statistics
if not st.session_state.data_history.empty:
    avg_heart_rate = st.session_state.data_history['heart_rate'].mean()
    avg_steps = st.session_state.data_history['steps'].mean()
    st.write(f"**Average Heart Rate:** {avg_heart_rate:.2f} bpm")
    st.write(f"**Average Steps:** {avg_steps:.2f} steps")

    # Get insights from GPT
    gpt_insights = get_gpt_insights(avg_heart_rate, avg_steps)
    st.subheader("Insights & Recommendations")
    st.write(gpt_insights)

# Option to clear history
if st.button("Clear History"):
    st.session_state.data_history = pd.DataFrame(columns=["timestamp", "heart_rate", "steps"])
    st.success("Data history cleared!")

# Footer
st.markdown("---")
st.markdown("This application was developed by **Joseff Tan**. 🤗")

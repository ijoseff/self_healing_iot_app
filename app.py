import streamlit as st
import json
from azure.iot.device import IoTHubDeviceClient
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

# Replace with your Azure IoT Hub connection string
IOT_HUB_CONNECTION_STRING = "HostName=simply-automate.azure-devices.net;DeviceId=simulated-device;SharedAccessKey=8gX1+FD9a0nOkXlinPZq1JvHYTEqmZqHpMvvMOUS6YU="

# Global DataFrame to store telemetry data
if 'data_history' not in st.session_state:
    st.session_state.data_history = pd.DataFrame(columns=["timestamp", "heart_rate", "steps"])

def get_device_data():
    # Logic to retrieve data from IoT Hub
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

# Function to plot the data
def plot_data():
    if not st.session_state.data_history.empty:
        st.line_chart(st.session_state.data_history.set_index('timestamp'))

st.set_page_config(page_title="Health Monitoring Dashboard", layout="wide")
st.title("Real-Time Health Monitoring Dashboard")
st.sidebar.header("Settings")
refresh_interval = st.sidebar.slider("Data Refresh Interval (seconds)", min_value=1, max_value=10, value=5)

# Simulated data display
if st.button('Get Latest Data'):
    data = get_device_data()
    # Append new data to history
    new_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['timestamp'])),
        "heart_rate": data['heart_rate'],
        "steps": data['steps']
    }
    st.session_state.data_history = st.session_state.data_history.append(new_data, ignore_index=True)

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

# Option to clear history
if st.button("Clear History"):
    st.session_state.data_history = pd.DataFrame(columns=["timestamp", "heart_rate", "steps"])
    st.success("Data history cleared!")

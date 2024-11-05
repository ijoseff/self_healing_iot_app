import streamlit as st
import json
from azure.iot.device import IoTHubDeviceClient
import random
import time
import pandas as pd
import plotly.graph_objects as go

# Define alert thresholds
HEART_RATE_THRESHOLD = 100
STEPS_THRESHOLD = 1000

# Azure IoT Hub connection string
IOT_HUB_CONNECTION_STRING = "HostName=simply-automate.azure-devices.net;DeviceId=simulated-device;SharedAccessKey=8gX1+FD9a0nOkXlinPZq1JvHYTEqmZqHpMvvMOUS6YU="

# Global DataFrame to store telemetry data
if 'data_history' not in st.session_state:
    st.session_state.data_history = pd.DataFrame(columns=["timestamp", "heart_rate", "steps"])

def get_device_data():
    heart_rate = random.randint(60, 120)  # Set a wider range to simulate alerts
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

    # Check for alert conditions
    if heart_rate > HEART_RATE_THRESHOLD:
        st.error(f"⚠️ Alert: Heart rate is unusually high at {heart_rate} bpm!")
    if steps < STEPS_THRESHOLD:
        st.warning(f"⚠️ Alert: Low steps detected today: {steps} steps.")

    return payload

# Streamlit page configuration
st.set_page_config(page_title="Health Monitoring Dashboard", layout="wide")
st.title("🏥 Real-Time Health Monitoring Dashboard")

# Button to retrieve latest data
if st.button('Get Latest Data'):
    with st.spinner('Fetching data from IoT Hub...'):
        data = get_device_data()
        new_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['timestamp'])),
            "heart_rate": data['heart_rate'],
            "steps": data['steps']
        }
        
        # Convert new_data to DataFrame and append to session history
        new_data_df = pd.DataFrame([new_data])
        st.session_state.data_history = pd.concat([st.session_state.data_history, new_data_df], ignore_index=True)

        st.success("Data retrieved successfully!")
        st.write(f"**Heart Rate:** {data['heart_rate']} bpm")
        st.write(f"**Steps:** {data['steps']} steps")
        st.write(f"**Timestamp:** {new_data['timestamp']}")

# Plot historical data
st.subheader("Historical Data")
plot_data()  # Existing function to plot data

# Additional metrics and insights
if not st.session_state.data_history.empty:
    avg_heart_rate = st.session_state.data_history['heart_rate'].mean()
    avg_steps = st.session_state.data_history['steps'].mean()
    st.write(f"**Average Heart Rate:** {avg_heart_rate:.2f} bpm")
    st.write(f"**Average Steps:** {avg_steps:.2f} steps")
    
    # Optionally, add more insights with GPT
    # insights = get_gpt_insights(avg_heart_rate, avg_steps)
    # st.info(insights)

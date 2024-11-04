import streamlit as st
import pandas as pd
import json
from azure.iot.hub import IoTHubRegistryManager
import random


# Replace with your Azure IoT Hub connection string
IOT_HUB_CONNECTION_STRING = "HostName=simply-automate.azure-devices.net;DeviceId=simulated-device;SharedAccessKey=8gX1+FD9a0nOkXlinPZq1JvHYTEqmZqHpMvvMOUS6YU="

def get_device_data():
    # Logic to retrieve data from IoT Hub
    # For demo purposes, this function will generate random data
    # In a real scenario, you'd fetch this from your Azure IoT Hub

    heart_rate = random.randint(60, 100)
    steps = random.randint(0, 10000)
    return {"heart_rate": heart_rate, "steps": steps, "timestamp": time.time()}

st.title("Real-Time Health Monitoring Dashboard")

# Simulated data display
if st.button('Get Latest Data'):
    data = get_device_data()
    st.write(f"Heart Rate: {data['heart_rate']}")
    st.write(f"Steps: {data['steps']}")
    st.write(f"Timestamp: {data['timestamp']}")


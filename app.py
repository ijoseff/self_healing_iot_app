import streamlit as st
import json
from azure.iot.device import IoTHubDeviceClient
import random
import time

# Replace with your Azure IoT Hub connection string
IOT_HUB_CONNECTION_STRING = "HostName=simply-automate.azure-devices.net;DeviceId=simulated-device;SharedAccessKey=8gX1+FD9a0nOkXlinPZq1JvHYTEqmZqHpMvvMOUS6YU="

def get_device_data():
    # Logic to retrieve data from IoT Hub
    # This example will send simulated data to the IoT Hub

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

st.title("Real-Time Health Monitoring Dashboard")

# Simulated data display
if st.button('Get Latest Data'):
    data = get_device_data()
    st.write(f"Heart Rate: {data['heart_rate']}")
    st.write(f"Steps: {data['steps']}")
    st.write(f"Timestamp: {data['timestamp']}")

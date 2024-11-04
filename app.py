import streamlit as st
from mqtt_client import create_mqtt_client
from gpt_response import get_gpt_solution

st.title("Self-Healing IoT Dashboard")

# Function to simulate device check and error handling
def check_device_status():
    # Simulate an error for demonstration
    issue = "Device temperature exceeds normal range"
    st.write(f"Detected issue: {issue}")

    # Use GPT to generate a self-healing solution
    solution = get_gpt_solution(issue)
    st.write(f"Suggested Solution: {solution}")

# Start MQTT client for real-time data (optional)
mqtt_client = create_mqtt_client()
mqtt_client.loop_start()

# Trigger self-healing check on button click
if st.button("Check Device Status"):
    check_device_status()

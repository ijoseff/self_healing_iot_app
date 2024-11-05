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

# Function to retrieve and send simulated device data
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
            marker=dict(color='#1f77b4')
        ))

        # Add steps trace
        fig.add_trace(go.Scatter(
            x=st.session_state.data_history['timestamp'],
            y=st.session_state.data_history['steps'],
            name='Steps',
            yaxis='y2',
            mode='lines+markers',
            marker=dict(color='#ff7f0e')
        ))

        # Update layout for dual axes
        fig.update_layout(
            title='📈 Health Monitoring Data',
            xaxis=dict(title='Timestamp'),
            yaxis=dict(title='Heart Rate (bpm)', side='left', showgrid=False),
            yaxis2=dict(title='Steps', side='right', overlaying='y', showgrid=False),
            legend=dict(x=0.1, y=0.9),
            template='plotly_white'
        )

        st.plotly_chart(fig)

# Streamlit page configuration
st.set_page_config(page_title="Health Monitoring Dashboard", layout="wide", initial_sidebar_state="collapsed")
st.title("🏥 Real-Time Health Monitoring Dashboard")

# Divider for Azure IoT Hub source notification
st.markdown("---")
st.write("🔗 **Data Source**: Pulling data from Azure IoT Hub")

# Divider for Live Data Update section
st.markdown("---")
st.subheader("🔄 Live Data Update")

# Button to retrieve latest data
if st.button('Get Latest Data'):
    with st.spinner('Fetching data from Azure IoT Hub...'):
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
        st.metric(label="Heart Rate", value=f"{data['heart_rate']} bpm")
        st.metric(label="Steps", value=f"{data['steps']} steps")
        st.write(f"**Timestamp:** {new_data['timestamp']}")

# Divider for Historical Data section
st.markdown("---")
st.subheader("📊 Historical Data")
plot_data()  # Calls the plot_data function defined above

# Divider for Key Insights section
st.markdown("---")
st.subheader("📈 Key Insights")
if not st.session_state.data_history.empty:
    avg_heart_rate = st.session_state.data_history['heart_rate'].mean()
    avg_steps = st.session_state.data_history['steps'].mean()
    
    col1, col2 = st.columns(2)
    col1.metric(label="Average Heart Rate", value=f"{avg_heart_rate:.2f} bpm")
    col2.metric(label="Average Steps", value=f"{avg_steps:.2f} steps")
    
    # Display progress towards daily step goal
    progress = min(100, int((avg_steps / STEPS_THRESHOLD) * 100))
    st.progress(progress)

    st.caption("Note: Health data is simulated for testing purposes.")
    st.caption("Developed by **Joseff Tan**". 🤗)

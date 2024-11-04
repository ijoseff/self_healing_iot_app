import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Replace with your connection string
CONNECTION_STRING = "HostName=simply-automate.azure-devices.net;DeviceId=simulated-device;SharedAccessKey=8gX1+FD9a0nOkXlinPZq1JvHYTEqmZqHpMvvMOUS6YU="

def create_device_client():
    return IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def send_device_to_cloud_messages():
    client = create_device_client()
    while True:
        heart_rate = random.randint(60, 100)  # Simulated heart rate
        steps = random.randint(0, 10000)  # Simulated steps
        data = {
            "heart_rate": heart_rate,
            "steps": steps,
            "timestamp": time.time()
        }
        message = Message(str(data))
        print(f"Sending message: {message}")
        client.send_message(message)
        time.sleep(5)  # Send a message every 5 seconds

if __name__ == "__main__":
    send_device_to_cloud_messages()

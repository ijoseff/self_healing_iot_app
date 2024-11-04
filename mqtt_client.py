import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully!")
        client.subscribe("device/status")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

def create_mqtt_client():
    # Create an MQTT client instance using WebSocket transport
    client = mqtt.Client(transport="websockets")
    
    # Attach event handlers
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Set up TLS/SSL
    client.tls_set()  # Ensures secure WebSocket connection

    # Attempt to connect to Azure IoT Hub using WebSockets on port 443
    client.connect("simply-automate.azure-devices.net", port=443, keepalive=60)
    
    return client

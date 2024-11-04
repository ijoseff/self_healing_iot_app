import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe("device/status")

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode())

def create_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("simply-automate.azure-devices.net", 1883, 60)
    return client

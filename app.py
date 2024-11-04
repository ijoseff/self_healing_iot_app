from mqtt_client import create_mqtt_client
from gpt_response import get_gpt_solution

def check_device_status():
    # Simulate receiving an error status from a device
    issue = "Device temperature exceeds normal range"
    print("Detected issue:", issue)

    # Attempt self-healing
    solution = get_gpt_solution(issue)
    print("Suggested Solution:", solution)

if __name__ == "__main__":
    mqtt_client = create_mqtt_client()
    mqtt_client.loop_start()  # Start MQTT loop

    # Run periodic checks (simplified for demo)
    check_device_status()

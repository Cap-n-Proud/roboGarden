import paho.mqtt.client as mqtt
import time
import json
import random

# MQTT broker configuration
broker_address = "192.168.1.121"
port = 1883
base_topic = "robogarden"

# Create an MQTT client
client = mqtt.Client("Publisher")

# Connect to the MQTT broker
client.connect(broker_address, port=port)

def publish_sensor_data(sensor_name, unit_of_measurement, device_class, icon, sensor_value):
    # Discovery message to create the sensor
    discovery_topic = f"homeassistant/sensor/{base_topic}/{sensor_name}/config"

    discovery_payload = {
        "name": sensor_name,
        "state_topic": f"{base_topic}/{sensor_name}",
        "unit_of_measurement": unit_of_measurement,
        "unique_id": f"robogarden_{sensor_name}",
        "device_class": device_class,
        "icon": icon,
        "device": {
            "identifiers": "robogarden001",
            "manufacturer": "Homemade",
            "model": "Base",
            "name": "Robogarden",
            "sw_version": "1.0"
        }
    }

    # Publish the discovery message for the sensor
    client.publish(discovery_topic, json.dumps(discovery_payload), retain=True)

    client.publish(f"{base_topic}/{sensor_name}", str(sensor_value))

# device class: https://www.home-assistant.io/integrations/sensor/#device-class

while True:
    # Start sending data for the Pump sensor with an initial value of 0
    value = random.randint(0, 100)
    publish_sensor_data(sensor_name="pump", unit_of_measurement="", device_class="battery", icon="mdi:pump", sensor_value=value)
    publish_sensor_data(sensor_name="light", unit_of_measurement="", device_class="battery", icon="mdi:lightbulb-on-outline", sensor_value=value)

    # Start sending data for the Program sensor with an initial value of 100
    value = random.randint(100, 999)
    publish_sensor_data(sensor_name="program", unit_of_measurement="", device_class="battery", icon="mdi:application-edit-outline", sensor_value=value)
    time.sleep(0.5)

# Keep the script running
# try:
#     client.loop_forever()
# except KeyboardInterrupt:
#     print("Script terminated by user.")
#     client.disconnect()

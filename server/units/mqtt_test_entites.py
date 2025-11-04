import paho.mqtt.client as mqtt
import time
import datetime
import json
import random  # Import the random module

# MQTT broker configuration
broker_address = "192.168.1.121"
port = 1883
base_topic = "robogarden"
device_name = "robogarden"

# Create an MQTT client
client = mqtt.Client("Publisher")

# Connect to the MQTT broker
client.connect(broker_address, port=port)

while True:
    # Generate random values for different entities
    random_value_1 = random.randint(1, 10)
    random_value_2 = random.randint(11, 20)

    # Discovery message to create the device
    device_discovery_topic = f"homeassistant/device/{device_name}/config"
    # device_discovery_topic = "homeassistant/sensor/my_mqtt_sensor/config"

    # device_discovery_payload = {
    #     "name": device_name,
    #     "model": "Base",
    #     "manufacturer": "Me",
    #     "identifiers": "robogarden-id",
    #     "sw_version": "1.0",
    # }

    device_discovery_payload = {
        "name": "Robogarden",
        "state_topic": base_topic,
        "unit_of_measurement": "",  # No unit of measurement for random integers
        "unique_id": "robogarden001",
        "device": {
            "identifiers": "robogarden001",
            "manufacturer": "Homemade",
            "model": "Base",
            "name": "Robogarden",
            "sw_version": "1.0",
        }
    }

    # Publish the device discovery message
    client.publish(device_discovery_topic,
                   json.dumps(device_discovery_payload))

    # Publish the random values for two different entities
    entity_1_topic = f"{base_topic}/pump"
    entity_2_topic = f"{base_topic}/program"

    client.publish(entity_1_topic, str(random_value_1))
    client.publish(entity_2_topic, str(random_value_2))

    # Wait for 1 second before sending the next message
    time.sleep(1)
    print(entity_1_topic, random_value_1, entity_2_topic, random_value_2,
          device_discovery_topic, device_discovery_payload)

# Disconnect from the broker (this will never be reached in this example)
client.disconnect()

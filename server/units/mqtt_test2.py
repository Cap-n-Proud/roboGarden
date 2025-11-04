import paho.mqtt.client as mqtt
import time
import datetime
import json
import random  # Import the random module


# MQTT broker configuration
broker_address = "192.168.1.121"
port = 1883
base_topic = "robogarden"

# Create an MQTT client
client = mqtt.Client("Publisher")

# Connect to the MQTT broker
client.connect(broker_address, port=port)

while True:
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 # Value message to send
    value_message = True
    # Generate a random integer between 1 and 10
    value_message1 = random.randint(1, 10)
    value_message2 = random.randint(11, 21)

    # Discovery message to create the sensor
    discovery_topic = "homeassistant/sensor/my_mqtt_sensor/config"
    # discovery_topic = "homeassistant"

    discovery_payload = {
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

    entity_1_topic = f"{base_topic}/pump"
    entity_2_topic = f"{base_topic}/program"

    # Publish the discovery message
    client.publish(discovery_topic, json.dumps(discovery_payload))

    # Publish the value message to the state topic
    client.publish(entity_1_topic, str(value_message1))

    # Publish the value message to the state topic
    client.publish(entity_2_topic, str(value_message2))

    print(entity_1_topic, value_message1, entity_2_topic,
          value_message2, base_topic, discovery_payload)
    # Wait for 1 second before sending the next message
    time.sleep(1)

# Disconnect from the broker (this will never be reached in this example)
client.disconnect()

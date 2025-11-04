import paho.mqtt.client as mqtt
import time
import datetime
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

# Discovery message to create the pump sensor
discovery_topic_pump = f"homeassistant/sensor/{base_topic}/pump/config"

discovery_payload_pump = {
    "name": "Pump",
    "state_topic": f"{base_topic}/pump",
    # Define a unit of measurement for the sensor (e.g., percentage)
    "unit_of_measurement": "%",
    "unique_id": "robogarden_pump",
    # Define a relevant device class (e.g., battery, moisture)
    "device_class": "battery",
    "device": {
        "identifiers": "robogarden001",
        "manufacturer": "Homemade",
        "model": "Base",
        "name": "Robogarden",
        "sw_version": "1.0"
    }
}

# Discovery message to create the program sensor
discovery_topic_program = f"homeassistant/sensor/{base_topic}/prg/config"

discovery_payload_program = {
    "name": "Prg",
    "state_topic": f"{base_topic}/prg",
    # Define a unit of measurement (e.g., seconds)
    "unit_of_measurement": "%",
    "unique_id": "robogarden_prg",
    # Define a relevant device class (e.g., timestamp)number
    "device_class": "battery",
    "device": {
        "identifiers": "robogarden001",
        "manufacturer": "Homemade",
        "model": "Base",
        "name": "Robogarden",
        "sw_version": "1.0"
    }
}

# Publish the discovery messages for the sensors
client.publish(discovery_topic_pump, json.dumps(
    discovery_payload_pump), retain=True)
client.publish(discovery_topic_program, json.dumps(
    discovery_payload_program), retain=True)

# Start a loop to publish random numbers to the MQTT topics
while True:

    # Generate random numbers for the pump and program entities
    pump_value = random.randint(0, 100)
    program_value = random.randint(100, 999)

    # Publish the random numbers to the MQTT topics
    client.publish(f"{base_topic}/pump", str(pump_value))
    client.publish(f"{base_topic}/prg", str(program_value))

    # Wait for 1 second before sending the next message
    time.sleep(1)

# Disconnect from the broker (this will never be reached in this example)
client.disconnect()

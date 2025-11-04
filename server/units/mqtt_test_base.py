import paho.mqtt.client as mqtt
import time
import datetime

# MQTT broker configuration
broker_address = "192.168.1.121"
port = 1883
topic = "robogarden/pump"

# Create an MQTT client
client = mqtt.Client("Publisher")

# Connect to the MQTT broker
client.connect(broker_address, port=port)

while True:
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Message to send
    message = f"Hello, MQTT! Timestamp: {timestamp}"

    # Publish the message to the topic
    client.publish(topic, message)

    # Wait for 1 second before sending the next message
    time.sleep(1)

# Disconnect from the broker (this will never be reached in this example)
client.disconnect()

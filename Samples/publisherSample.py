import paho.mqtt.client as mqtt
import random
import time
import json
from datetime import datetime

# Set broker cloud url
mqttBroker = "mqtt.eclipseprojects.io"

# Set up as mqtt client with the name "Temperature_Inside_Sensor" 
# this is the name of the client publishing to the broker
client = mqtt.Client("Temperature_Inside_Sensor")

# inifnite loop to connect the client to mqtt server and send the desired messages
while True:

    # Connect client to the broker
    client.connect(mqttBroker)

    # Create a random float between 20.0 - 25.0
    randomValue = random.uniform(20.0, 25.0)

    # Store current timestamp and the value in a dictionary
    message = {
        "timestamp": str(datetime.now()),
        "temp": randomValue
    }

    # Convert the dictionary to a json
    jsonedMessage = json.dumps(message)

    # publish the json message to the "TEMP" topic which subscribers listen to 
    # temp short for temperature
    client.publish("TEMP", jsonedMessage)

    # prints out the json file being sent to the broker and the topic its going to
    print("Published to broker: " + jsonedMessage +
            "\nTopic:" + " TEMP\n")

    # disconnect client from broker
    client.disconnect()

    # rest for 2 seconds and repeat due to infinite while loop
    time.sleep(2)


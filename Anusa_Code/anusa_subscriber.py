# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 23:52:50 2022

@author: anusa
"""

import paho.mqtt.client as mqtt
import time
import json

# callback function from the client.on_message = on_message (line 21) to display the message 
# can be used to return the message to a graph to plot 
def on_message(client, userdata, message):
    # converts the message from a mqtt object to the json object we sent
    # and converts the json object back to a dictionary in one line
    msg = json.loads(message.payload.decode("utf-8"))

    # prints the msg dictionary values in coresponding keys (timestamp, temp) which we sent from publisher
    print("Received Message: " + str(msg["NOK-Stock"]) + "\nTimestamp: " + str(msg["timestamp"]) + "\n")

# Set broker cloud url
mqttBroker ="mqtt.eclipseprojects.io"

# set topics as tuple pairs with ("topic name", "Quality of Service value") 
# keep the QoS value to 0 for any new topics
# adding new topic is simple as topics = [("TEMP", 0), ("New_Topic", 0)]
topics = [("Stock_Details", 0)]

# Set up a new mqtt client and naming it "Smartphone" 
# can be named anything 
# this is an example if the subsciber is from a smartphone
client = mqtt.Client("Smartphone")

# connect the mqtt client to the broker server
client.connect(mqttBroker) 

# Mandatory loop to start the receiving process
# everything happens inside this loop to receive the data from the topics sent by the publishers
client.loop_start()

# subscribe the client to the topics
client.subscribe(topics)

# callback function for the on_message method when a message was received from broker 
# a message will be received once the publisher sends a message to the broker
client.on_message = on_message 

#loop will continue until this timer is done then goes to the next call at line 42 to end the program
time.sleep(30)

# client is finished and the program ends once the time.sleep() is finished
client.loop_stop()
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:52:17 2022

@author: joshua
"""

import paho.mqtt.client as mqtt
import time
import json
import matplotlib.pyplot as plt

# from group_3_publisher_1 import Publisher

class Subscriber():
    def __init__(self):
        '''
        Initialize a list to store all the values we receive from a Publisher

        Returns
        -------
        None.

        '''
        self.values = []
        self.timestamps = []
    
    def on_message(self, client, userdata, message):
        '''
        to-do

        Parameters
        ----------
        client : TYPE
            DESCRIPTION.
        userdata : TYPE
            DESCRIPTION.
        message : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        # converts the message from a mqtt object to the json object we sent
        # and converts the json object back to a dictionary in one line
        msg = json.loads(message.payload.decode("utf-8"))
        if (message.topic == "TEMP"):
            self.values.append(msg["y-value"])
            self.timestamps.append(msg["timestamp"])
    
        # prints the msg dictionary values in coresponding keys (timestamp, temp) which we sent from publisher
        print("Received Message: " + str(msg["y-value"]) + "\nTimestamp: " + str(msg["timestamp"]) + "\n")

    
    def post(self):
        '''
        to-do

        Returns
        -------
        None.

        '''
        # Set broker cloud url
        mqttBroker ="mqtt.eclipseprojects.io"
        
        # set topics as tuple pairs with ("topic name", "Quality of Service value") 
        # keep the QoS value to 0 for any new topics
        # adding new topic is simple as topics = [("TEMP", 0), ("New_Topic", 0)]
        topics = [("AMPLITUDE", 0)]
        
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
        client.on_message = self.on_message 
        
        #loop will continue until this timer is done then goes to the next call at line 42 to end the program
        time.sleep(30)
        
        
        # Plot list of values
        fig, ax = plt.subplots()
        plt.xlabel("Time")
        plt.ylabel("y-value")
        plt.plot(self.timestamps, self.values)
        every_nth = 4
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        
        # client is finished and the program ends once the time.sleep() is finished
        client.loop_stop()
        
        
'''
TESTING PURPOSES
'''
def main():
    s = Subscriber()
    s.post()

if __name__ == "__main__":
    main()
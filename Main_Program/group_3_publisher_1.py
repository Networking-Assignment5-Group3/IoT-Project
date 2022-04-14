# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 15:38:30 2022

@author: joshua
"""

import numpy as np
import math
import random
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime


class Publisher():
    def generate_value(self):
        '''
        Generates a random value and a timestamp for that value.
        Values generated are based on a sin wave pattern.
        
        Returns
        -------
        None
        
        '''
        time = np.arange(0,2*math.pi,math.pi/10)
        amplitude = np.sin(time)
        self.value = random.choice(amplitude)
        self.timestamp = datetime.now().strftime('%M:%S.%f')[:-4]
    
    
    def json_package(self):
        '''
        Create a json object with the generated value and timestamp.

        Returns
        -------
        None.

        '''
        self.data = {
                "y-value" : self.value, "timestamp" : self.timestamp
            }
    
    
    def save_json(self):
        '''
        Dump the dict object into a json object.

        Returns
        -------
        None.

        '''
        self.jsonData = json.dumps(self.data,default=str)
    
    
    def publish(self):
        # Set broker cloud url
        mqttBroker = "mqtt.eclipseprojects.io"
        
        # Set up as mqtt client with the name "Sin_Wave" 
        # this is the name of the client publishing to the broker
        client = mqtt.Client("Sin_Wave")
        
        while True:
            # Connect client to the broker
            client.connect(mqttBroker)
            
            # Generate a random value from a sin wave
            self.generate_value()
            
            # Store current timestamp and the value in a dictionary
            self.json_package()
            
            # Convert the dictionary to a json
            self.save_json()
            
            # publish the json message to the "AMPLITUDE" topic which subscribers listen to 
            client.publish("AMPLITUDE", self.jsonData)
        
        
            # prints out the json file being sent to the broker and the topic its going to
            print("Published to broker: " + self.jsonData +
                    "\nTopic:" + " Amplitude\n")
            
            # disconnect client from broker
            client.disconnect()
            
            # rest for 2 seconds and repeat due to infinite while loop
            time.sleep(2)
        
'''
TESTING PURPOSES
'''
def __main__():
    p = Publisher()
    p.publish()

if __name__ == "__main__":
    __main__()

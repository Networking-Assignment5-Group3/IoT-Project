# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 22:03:30 2022

@author: anusa
"""
#Publisher 2
import numpy as np
import random
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime

    
class Publisher():

    def generate_value(self) -> int:
        '''
        Generates a random value and a timestamp for that value.
        Values generated are based on a stock.
        
        Returns
        -------
        int
        
        '''
        def growth(series):
            m = random.random()
            return series * m

        def oscillation(i):
            delta = random.random() - 1
            coeff = random.randint(1,10)
            return i + (coeff * delta)

        series = growth(np.array(range(10)))
        array_series = np.array([oscillation(i) for i in series])
        
        
        stock_series = ((array_series - array_series.mean()) / (array_series.max() - array_series.min())) + 1
        self.stock_series = random.choice(stock_series)
        self.timestamp = datetime.now()
        
       
    def json_package(self):
        '''
        Create a json object with the generated value and timestamp.

        Returns
        -------
        None.

        '''
        self.data = {
                "NOK-Stock" : self.stock_series, "timestamp" : self.timestamp
            }
    
    
    def save_json(self):
        '''
        Dump the json object into a .json file.

        Returns
        -------
        None.

        '''
        self.jsonData = json.dumps(self.data,default=str)
    
    def publish(self):
        # Set broker cloud url
        mqttBroker = "mqtt.eclipseprojects.io"
        
        # Set up as mqtt client with the name "Stock_Details" 
        # this is the name of the client publishing to the broker
        client = mqtt.Client("Stock_Details")
        
        while True:
            # Connect client to the broker
            client.connect(mqttBroker)
            
            # Create a random float between 20.0 - 25.0
            randomValue = random.uniform(10.0, 15.0)
            
            message = {
                "timestamp": str(datetime.now()),
                "NOK-Stock": randomValue
                }
            
            # Convert the dictionary to a json
            jsonedMessage = json.dumps(message)

            # Generate a random value from a stock
            self.generate_value()
      
            # Store current timestamp and the value in a dictionary
            self.json_package()
      
            # Convert the dictionary to a json
            self.save_json()
            
            # publish the json message to the "TEMP" topic which subscribers listen to 
            client.publish("Stock_Details", jsonedMessage)

            # prints out the json file being sent to the broker and the topic its going to
            print("Published to broker: " + jsonedMessage +
            "\nTopic:" + " Stock_Details\n")
              
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

   
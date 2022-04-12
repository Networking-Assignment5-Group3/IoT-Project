# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 15:38:30 2022

@author: joshua
"""

import numpy as np
import math
import random
import json
from datetime import datetime


class Publisher():
    def generate_value(self) -> int:
        '''
        Generates a random value and a timestamp for that value.
        Values generated are based on a sin wave pattern.
        
        Returns
        -------
        int
        
        '''
        time = np.arange(0,2*math.pi,math.pi/10)
        amplitude = np.sin(time)
        self.value = random.choice(amplitude)
        self.timestamp = datetime.now()
    
    
    def json_package(self):
        '''
        Create a json object with the generated value and timestamp.

        Returns
        -------
        None.

        '''
        self.data = {
                "value" : self.value, "timestamp" : self.timestamp
            }
    
    
    def save_json(self):
        '''
        Dump the json object into a .json file.

        Returns
        -------
        None.

        '''
        jsonData = json.dumps(self.data,default=str)
        with open("package.json",'w') as f:
            f.write(jsonData)
        
        
        
'''
TESTING PURPOSES
'''
def __main__():
    p = Publisher()
    p.generate_value()
    print("Chosen value: ", p.value)
    print("Timestamp: ", p.timestamp)
    p.json_package()
    p.save_json()

if __name__ == "__main__":
    __main__()

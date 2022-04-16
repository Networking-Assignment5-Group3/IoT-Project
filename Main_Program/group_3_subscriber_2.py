# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:52:17 2022

@author: joshua
"""

import paho.mqtt.client as mqtt
import time
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Subscriber():
    def __init__(self):
        '''
        Initialize a list to store all the values we receive from a Publisher

        Returns
        -------
        None.
        '''
        self.oscillation_values = []
        self.oscillation_timestamps = []

        self.amplitude_values = []
        self.amplitude_timestamps = []
        self.fig, self.ax = plt.subplots(1,2)

    # called by ani variable in self.post()
    # removes last element in values and timestamps once length of values reaches 5
    def animate(self, i):
        # clear axis
        self.ax[0].clear()
        self.ax[1].clear()

        # once values length reaches 5 then remove first element of values and timestamps
        if (len(self.oscillation_values) == 16):
            self.oscillation_values.pop(0)
            self.oscillation_timestamps.pop(0)

        if (len(self.amplitude_values) == 6):
            self.amplitude_values.pop(0)
            self.amplitude_timestamps.pop(0)

        # plot axis of Oscillation
        self.ax[0].plot(self.oscillation_timestamps, self.oscillation_values)

        # plot axis of Amplitude
        self.ax[1].plot(self.amplitude_timestamps, self.amplitude_values)



        # label axis
        self.ax[0].set_xlabel("Time")
        self.ax[0].set_ylabel("Oscillations")
        self.ax[0].set_title ("Oscillation Time Graph")

        self.ax[1].set_xlabel("Time")
        self.ax[1].set_ylabel("Amplitude")
        self.ax[1].set_title("Amplitude Time Graph")

        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = "10"
        plt.setp(self.ax[0].get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.setp(self.ax[1].get_xticklabels(), rotation=30, horizontalalignment='right')

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
        if (message.topic == "OSCILLATIONS"):
            self.oscillation_values.append(msg["y-value"])
            self.oscillation_timestamps.append(msg["timestamp"])

        if (message.topic == "AMPLITUDE"):
            self.amplitude_values.append(msg["y-value"])
            self.amplitude_timestamps.append(msg["timestamp"])

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
        mqttBroker = "mqtt.eclipseprojects.io"

        # set topics as tuple pairs with ("topic name", "Quality of Service value")
        # keep the QoS value to 0 for any new topics
        # adding new topic is simple as topics = [("TEMP", 0), ("New_Topic", 0)]
        topics = [("OSCILLATIONS", 0),("AMPLITUDE", 1)]

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

        # calls the animate method to add each variables to the plot and display it
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)

        plt.show()

        # loop will continue until this timer is done then goes to the next call at line 42 to end the program
        time.sleep(30)

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
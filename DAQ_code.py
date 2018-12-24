#SCRIPT TO SEND DATA FROM RASPBERRY PI TO THE AWS SERVER
#Written by Anoush Sepehri in collaboration with the University of Manitoba Fluid Power and TeleRobotics Research Laboratory
# CHECK README FOR FUNCTION DEFINITIONS AND PROPOGATIONS
#! /usr/bin/env python


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import RPi.GPIO as IO
import Adafruit_ADS1x15
import datetime
import pytz
import socket
import zlib
import gzip
import base64
import sys
import user_functions as uf

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(21,IO.OUT)
IO.setup(26,IO.OUT)
IO.setup(20, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(16, IO.IN, pull_up_down=IO.PUD_UP)

timespanInterval = 120 #change depending on how long DAQ will take place
postingInterval = 120 
updateInterval = 0.01 #100 Hz sampling rate
DAQtime=6000 #DAQ EVERY SET SECONDS

adc = Adafruit_ADS1x15.ADS1115() #ADC identification
lastConnectionTime=time.time()
lastUpdateTime=time.time()
intialtime=time.time()
recordingInterval=time.time()
payload = []
messageBuffer = {}
timesave=0
lastupdate=0
ident=0
count=0

myMQTTClient = AWSIoTMQTTClient("aws_thing1")
myMQTTClient.configureEndpoint("ase8a56yxgsqk.iot.us-east-2.amazonaws.com", 8883) #link to the amazon webservice client to recieve the information
myMQTTClient.configureCredentials("/home/pi/Downloads/connect_device_package/root-CA.crt", "/home/pi/Downloads/connect_device_package/aws_thing1.private.key", "/home/pi/Downloads/connect_device_package/aws_thing1.cert.pem") #location for certificate files and identification of raspberry pi

myMQTTClient.configureOfflinePublishQueueing(-1) 
myMQTTClient.configureDrainingFrequency(2) 
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)


while 1:

        check= uf.internet_check()
        if check==True and ident!=0:
                
                IO.output(26,IO.HIGH)
                myMQTTClient.connect()
                senddata()
                ident=0
                myMQTTClient.disconnect()
                IO.output(26,IO.LOW)

        if IO.input(20)==0 and IO.input(16)==0:
                IO.output(21,IO.HIGH)
                IO.output(26,IO.HIGH)
                time.sleep(1)
                IO.output(21,IO.LOW)
                IO.output(26,IO.LOW)
                exit()
                     

        elif IO.input(20)==0:
                
                IO.output(21,IO.HIGH)
                uf.intro()
                lastConnectionTime = time.time()
                lastUpdateTime = time.time()
                intialtime=time.time()
                uf.updatepayload()
                recordingInterval=time.time()
                payload=[]
                count=count+1
                IO.output(21,IO.LOW)

                while 1:
                        check=internet_check()

                        if check==True and ident!=0:
                                IO.output(26,IO.HIGH)
                                myMQTTClient.connect()
                                uf.senddata()
                                ident=0
                                myMQTTClient.disconnect()
                                IO.output(26,IO.LOW)
                

                        if time.time()-recordingInterval>=DAQtime:
                                IO.output(21,IO.HIGH)
                                uf.intro()
                                lastConnectionTime = time.time()
                                lastUpdateTime = time.time()
                                intialtime=time.time()
                                uf.updatepayload()
                                recordingInterval=time.time()
                                payload=[]
                                count=count+1
                                IO.output(21,IO.LOW)

                        if IO.input(16)==0:
                                break
   



    

 

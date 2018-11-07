#SCRIPT TO SEND DATA FROM RASPBERRY PI TO THE AWS SERVER
# CHECK README FOR FUNCTION DEFINITIONS AND PROPOGATIONS
#! /usr/bin/env python


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from datetime import date, datetime
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
import collections

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(21,IO.OUT)
IO.setup(26,IO.OUT)
IO.setup(20, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(16, IO.IN, pull_up_down=IO.PUD_UP)

timespanInterval = 120 #change depending on how long DAQ will take place
postingInterval = 120 
updateInterval = 0.01 #100 Hz sampling rate
DAQtime=180 #DAQ EVERY 2 HOURS

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




################################FUNCTIONS TO CALL############################################



def internet_check():
        try:
            host = socket.gethostbyname("www.google.com")
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False


def getdata():
    start=time.time()
    resolution=4.096/32767
    gain = 2.815

    x=adc.read_adc(0,1,data_rate=860)
    y=adc.read_adc(1,1,data_rate=860)
    #z=adc.read_adc_difference(3,1,data_rate=860)

    signal1 = round(x*resolution*gain,2)
    
    signal2 = round(y*resolution*gain,2)

    #signal3 = round(z*resolution,2)

    while 1:
        if time.time()-start>=updateInterval:
            return signal1, signal2

def updatepayload():
    while 1:
        global lastUpdateTime
        global initialtime
        global payload
        global messageBuffer
        global timesave
        global lastConnectionTime
        
        plot= round(time.time() - lastConnectionTime + timesave,2)
        signal,signal2 = getdata()

        messageBuffer['time']= plot
        messageBuffer['signal1']=signal
        messageBuffer['signal2']=signal2
        #messageBuffer['signal3']=signal3

        payload.append(messageBuffer)
        messageBuffer={}

        if time.time()-lastConnectionTime>= postingInterval:
            store_data()
            lastConnectionTime=time.time()
            
        if time.time()-lastConnectionTime+timesave >= timespanInterval+1: 
            timesave=0
            return


def store_data():
    global ident
    global lastConnectionTime
    global timesave
    global payload
    
    timesave= timesave + (time.time() - lastConnectionTime)
    identstr=str(ident)
    filename="data"+identstr+".txt"
    with open(filename, 'w') as outfile:
        json.dump(payload, outfile)
    ident=ident+1
    payload=[]


def senddata():
    global ident
    
    count=0
    for count in range(0,ident):
        text="data"+str(count)+".txt"
        with open(text) as infile:
            payload = json.load(infile)
        data=(json.dumps(payload,separators=(',', ':')))
        data=data.encode('utf-8')
        data=base64.b64encode(zlib.compress(data,9))
        data=data.decode("utf-8")
        myMQTTClient.publish("data", data, 0)
        time.sleep(1)
    count=0
    
def get_date():
    utc_now=pytz.utc.localize(datetime.datetime.utcnow())
    Cet_now=utc_now.astimezone(pytz.timezone('Canada/Central'))
    date=Cet_now.strftime("%Y/%m/%d %H:%M:%S")
    return date


def intro():
    global lastConncetionTime
    global lastUpdateTime
    global intialtime
    global messageBuffer

    date=get_date()
    print (date)
    messageBuffer={}
    messageBuffer['Machine']='Tractor: ' + date

        
###########################################SCRIPT###########################################

while 1:

        check= internet_check()
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
                intro()
                lastConnectionTime = time.time()
                lastUpdateTime = time.time()
                intialtime=time.time()
                updatepayload()
                recordingInterval=time.time()
                payload=[]
                count=count+1
                IO.output(21,IO.LOW)

                while 1:
                        check=internet_check()

                        if check==True and ident!=0:
                                IO.output(26,IO.HIGH)
                                myMQTTClient.connect()
                                senddata()
                                ident=0
                                myMQTTClient.disconnect()
                                IO.output(26,IO.LOW)
                

                        if time.time()-recordingInterval>=DAQtime:
                                IO.output(21,IO.HIGH)
                                intro()
                                lastConnectionTime = time.time()
                                lastUpdateTime = time.time()
                                intialtime=time.time()
                                updatepayload()
                                recordingInterval=time.time()
                                payload=[]
                                count=count+1
                                IO.output(21,IO.LOW)

                        if IO.input(16)==0:
                                break
   



    

 

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
    while True:
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
        messageBuffer['signal3']=signal3

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



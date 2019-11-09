from nanpy import (ArduinoApi, SerialManager, Stepper)
import time
import datetime
from random import randrange
import os,sys
run =False


# Initialize reed switch Pins #
reed_switch=[];
ticks=[];
volume=[];
Files=[]
Counters=[]

for i in range(30):
    Files.append(" ")
    Counters.append(" ")

init=22;
for i in range(30):
    reed_switch.append(init);
    volume.append(0);
    init=init+1;
    date=str(datetime.datetime.now().date())
    number=str(i+1)
    Files[i]=date+" - GC"+number+".csv"
    Counters[i]="Gas Counter "+number;

# here=Files[0].split(" ")
# dateo=datetime.datetime.now().date()
# dateob = datetime.datetime.strptime(here[0], '%Y-%m-%d').date()
# numb=(dateo-dateob).days
# print(numb)

## CONNECT FUNCTION ##
def ArdConnect(com):
    global run
    run = True
    try:
        #print('Connecting...')
        connection = SerialManager(device=com)
        ard = ArduinoApi(connection=connection)
        print("Device connected")
        return ard
    except:
        run=False
        print("Connection Failed!")
        return 'EMPTY'

# ## SETUP Arduino with the reed switch pins ##
def ArdSetup(ard):
     global run
     run = True
     try:
         for i in range(30):        
            ard.pinMode(reed_switch[i], ard.INPUT)
            print('pin #'+reed_switch[i]+' is set')
     except:
         run=False
         print("Setup Failed!")


## Get switch readings from the gas counters
def ReadSwitch(ard):
    global run
    run = True
    try:
        for i in range(30):
            ticks[i]=ard.digitalRead(reed_switch[i])
            return ticks
    except:
        run=False
        print("Switch readings Failed!")

folder="Counter_Logs"
if not os.path.exists(folder):
        os.mkdir(folder)
        for i in range(30):
            filePath=folder+"\\"+Files[i]
            open(filePath, 'a').close()
            fd = os.open(filePath,os.O_RDWR)
            firstRow=str.encode("Date-Time,Volume\n");
            os.write(fd,firstRow)
            os.close(fd) 

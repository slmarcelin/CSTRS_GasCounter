#Refer to main python file for references
from nanpy import (ArduinoApi, SerialManager, Stepper)
import time
import datetime
from random import randrange
import os,sys
import glob
import csv
run =False


# Initialize arrays #
reed_switch=[];
ticks=[];
volume=[];
Files=[]
allFiles=[]
Counters=[]

for i in range(30):
    Files.append(" ")
    Counters.append(" ")
    allFiles.append(" ")

#First input pin for Gas Counter
init=22;
for i in range(30):
    reed_switch.append(init);
    volume.append(0);
    init=init+1;
    date=str(datetime.datetime.now().date())
    number=str(i+1)
    Counters[i]="Gas Counter "+number;

## CONNECT FUNCTION ##
def ArdConnect(com):
    global run
    try:
        #print('Connecting...')
        connection = SerialManager(device=com)
        ard = ArduinoApi(connection=connection)
        print("[Arduino connected]")
        run = True
        return ard
    except:
        run=False
        print('[Connection Failed]')
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
         print('[Arduino setup...Failed]')


## Get switch readings from the gas counters
def ReadSwitch(ard):
    global run
    try:
        for i in range(30):
            ticks[i]=ard.digitalRead(reed_switch[i])
            run = True
            return ticks
    except:
        run=False
        print("Switch readings Failed!")

#Folder that holds all the csv files
folder="Counter_Logs"
#This is a very fragile if statement! Please do not change anything without consulting me
#This can mess up the entire program
#this if statement creates the folder if it does not exist as well as the files
if not os.path.exists(folder):
        os.mkdir(folder)
        for i in range(30):
            Files[i]=date+" - GC"+str(i+1)+".csv"
            allFiles[i]=Files[i]
            filePath=folder+"\\"+Files[i]
            open(filePath, 'a').close()
            fd = os.open(filePath,os.O_RDWR)
            firstRow=str.encode("Date-Time,Volume\n");
            os.write(fd,firstRow) 
            os.close(fd) 
            if(i==29): #Very important, all the file names are saved in a csv file
                filePath=folder+"\\"+"setup.csv"
                open(filePath, 'a').close()
                fd = os.open(filePath,os.O_RDWR)
                for k in range(30):
                    firstRow=str.encode(Files[k]+",");
                    os.write(fd,firstRow)

#Put all the file names inside a folder for application purposes
filePath=folder+"\\"+"setup.csv"
with open(filePath, newline='') as csvfile:
    Files= list(csv.reader(csvfile))




#Refer to main python file for references
from nanpy import (ArduinoApi, SerialManager, Stepper)
import time
import datetime
import threading
from random import randrange
import os,sys
import glob
import csv
run =False


# Initialize arrays #
reed_switch=[];
previousTicks=[1]*30;
ticks=[0]*30;
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
        print('\nAttempting to connect')
        print('Connecting...')
        connection = SerialManager(device=com)
        ard = ArduinoApi(connection=connection)
        print("Arduino connected")
        run = True
        return ard
    except:
        run=False
        print('Error :Connection Failed!!')
        return 'EMPTY'

# ## SETUP Arduino with the reed switch pins ##
def ArdSetup(ard):
     global run
     run = True
     try:
        # UNCOMMENT FOR ARDUINO MEGA
        for i in range(30): 
            ard.pinMode(reed_switch[i], ard.OUTPUT)
            ard.digitalWrite(reed_switch[i], ard.HIGH)
            print('pin #'+str(reed_switch[i])+' is set')
     except:
         run=False
         print('[Arduino setup...Failed]')

# ## Get switch readings from the gas counters
# def ReadSwitch(ard):
#     global run
#     try:
#         # UNCOMMENT FOR ARDUINO MEGA
#         for i in range(30):
#             ticks[i]=ard.digitalRead(reed_switch[i])
#             run = True
#     except:
#         run=False
#         print("Switch readings Failed!")

def ReadSwitch(ard,PinId):
    global run
    try:
        # UNCOMMENT FOR ARDUINO MEGA
        Pid=int(PinId)
        ticks[Pid-22]=ard.digitalRead(Pid)
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
        fd = open(filePath,'a')
        firstRow = "Date-Time,Volume\n"
        fd.write(str(firstRow))
        fd.flush()
        fd.close() 

        if(i==29): #Very important, all the file names are saved in a csv file
            filePath=folder+"\\"+"setup.csv"
            open(filePath, 'a').close()
            fd = os.open(filePath,os.O_RDWR)
            for k in range(30):
                firstRow=str.encode(Files[k]+",");
                os.write(fd,firstRow)
            os.close(fd)

if os.path.exists(folder):    
    #Put all the file names inside a folder for application purposes
    filePath=folder+"\\"+"setup.csv"
    with open(filePath, newline='') as csvfile:
        Files= list(csv.reader(csvfile))




class MyThread(threading.Thread): #Each of the 
    def run(self):
        global A
        while True:
            if run :  #If the arduino is running check all counters at the same time and do debouncing
                value=int(self.getName())           
                # print("Reading Pin Id {} started!".format(value))        # "Thread-x started!"
                connectS="CXN"
                ReadSwitch(A,value)  #Read the inputs
                index=value-22
                # print("Previous ticks for pin "+str(value))
                # print(ticks[index])
                cur=ticks[index]

                if (cur==0):
                    print("Volume increased for Counter of pin ID:"+str(value))
                    print(ticks[index])
                    time.sleep(2)
                    ticks[index]=1

                time.sleep(0.02) 
                                                     

            else:
                print("Port selected:" +com)
                A = ArdConnect(com)
                if run:
                    ArdSetup(A)
                    connectS="CXN"

def main():
    global A
    # for x in range(10,21):                                                 
    mythread = MyThread(name = format(40))  
    mythread1 = MyThread(name = format(36))
    mythread2 = MyThread(name = format(32))
    mythread.start()
    mythread1.start()
    mythread2.start()
    time.sleep(.9)                                   

global A
com = 'COM13'  #Change value for troubleshooting 
print("Port selected:" +com)
A = ArdConnect(com)
ArdSetup(A)
main()

# while True:
#     if run:
#         ReadSwitch(A,40)
#         print(A.digitalRead(40))
#         time.sleep(0.07) 




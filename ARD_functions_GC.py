
#Refer to main python file for references
from nanpy import (ArduinoApi, SerialManager, Stepper)
import time
import datetime
import threading
import os,sys
import glob
import csv
from pathlib import Path


run =False #Boolean flag which checks if the arduino is connected


# Initialize arrays #
reed_switch=[];  #Will contain the list of all switch pin numbers
ticks=[0]*30;    #Will contain the pin reading outputs
volume=[];       #For each tick, volume will be increased
Files=[]         #Files contains the names of the files
allFiles=[]      #Troubleshooting array of files
Counters=[]

for i in range(30):  #For loop goes from 0-29 because we have 30 gas counters
    Files.append(" ")  #Initialize the arrays
    allFiles.append(" ")
    Counters.append(" ")

init=22; #First input pin number for first Gas Counter
for i in range(30):
    reed_switch.append(init); #Append the pin numbers to the reed_switch array
    volume.append(0); #Initialize the volume array to 0
    init=init+1;       #Increase the pin id number
    number=str(i+1)
    Counters[i]="Gas Counter "+number;

## CONNECT FUNCTION ##
def ArdConnect(com):
    global run
    try:
        print('\nAttempting to connect to the given port -> '+com) #Print message to user
        print('Connecting...')
        connection = SerialManager(device=com)  #Connected to the provided serial com name
        ard = ArduinoApi(connection=connection) #Connect to the arduino
        print("Arduino connected")    #Print message to user
        run = True   #set run flag to true
        return ard   #return the arduino object
    except:
        run=False  #if tiem runs out set flag to False
        print('Error :Connection Failed!!') #Print message to user
        return 'EMPTY'  #Return an empty object(String)

# ## SETUP Arduino with the reed switch pins ##
def ArdSetup(ard):
     global run
     run = True  #Set initial run flag to be true
     try:
        for i in range(30): 
            ard.pinMode(reed_switch[i], ard.OUTPUT) #Set the pins as outputs
            ard.digitalWrite(reed_switch[i], ard.HIGH) #Write the pins to high
            print('pin # '+str(reed_switch[i])+' is set') #Print pin check message to user
     except:
         run=False  #else set flag to False
         print('[Arduino setup...Failed]') #Print error message to user

## Reads the pin status from the Arduino###
def ReadSwitch(ard,PinId):
    global run
    try:
        Pid=int(PinId) #convert the passed pin id to integer
        ticks[Pid-22]=ard.digitalRead(Pid) #Read the pin value and write to array
    except:
        run=False  #If error occured
        print("Switch readings Failed!") #Let user know that the readings failed


#Folder that holds all the csv files
folder="Counter_Logs"
folder = '{}/{}'.format(Path(__file__).parent.absolute(),'Counter_Logs')


#This is a very fragile if statement! Please do not change anything
#This can mess up the entire program
#this if statement creates the folder if it does not exist as well as the files
date=str(datetime.datetime.now().date()) #Get today's date
if not os.path.exists(folder): #If the folder does not exist
    os.mkdir(folder)  #create the folder
    for i in range(30):
        Files[i]=date+" - GC"+str(i+1)+".csv" #Create the names of the files
       
        allFiles[i]=Files[i]  #place file names in troubleshooting array
        filePath=folder+"\\"+Files[i]  #Get the new filepath by combining the folder name and new file name
        fd = open(filePath,'a')  #create file
        firstRow = "Date-Time,Volume\n" #create first line to file or in our case first two columns
        fd.write(str(firstRow))  #write first line to file
        fd.flush()
        fd.close()  #close the current file 

        if(i==29): #Very important, all the file names are saved in a csv file
            filePath=folder+"\\"+"setup.csv" #setup.csv contains all the files
            open(filePath, 'a').close() #It is important to keep the names accessible to the program
            fd = os.open(filePath,os.O_RDWR)
            for k in range(30):
                firstRow=str.encode(Files[k]+","); #Write filenames to setup.csv
                os.write(fd,firstRow)
            os.close(fd) #Close the file

if os.path.exists(folder): #If the folder exists, get the list of all file names
    #Put all the file names inside an array for application purposes
    filePath=folder+"\\"+"setup.csv"
    with open(filePath, newline='') as csvfile:
        Files= list(csv.reader(csvfile)) #This array will be called throughout the program to access the files


###########################################################################################################################
#                                                 CODE ONLINE REFERENCES
#  Title: Tutorial: Time Series Analysis with Pandas
#  Author: Jennifer Walker
#  Date Posted: January 10, 2019
#  Availability: https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/

#  Title: Using Tkinter and Matplotlib
#  Author: Ishan Bhargava
#  Date Posted: January 1, 2019
#  Availability: https://ishantheperson.github.io/posts/tkinter-matplotlib/

#  Title: Drop-down list (Combobox) in Tcl / Tk (tkinter)
#  Author: Python Resources 
#  Date Posted: June 16, 2017
#  Availability: https://recursospython.com/guias-y-manuales/lista-desplegable-combobox-en-tkinter/

#  Title: TypeError: Unrecognized value type: <class 'str'>
#  Author: jezrael 
#  Date Posted: May 27, 2018
#  Availability: https://stackoverflow.com/questions/50554107/typeerror-unrecognized-value-type-class-str

#  Title: tkinter button command runs function without clicking? 
#  Author: Eric Levieil
#  Date Posted: May 8, 2015
#  Availability: https://stackoverflow.com/questions/30129359/tkinter-button-command-runs-function-without-clicking

#  Title: How to import a csv-file into a data array?
#  Author: martineau
#  Date Posted: Oct 6, 2017
#  Availability: https://stackoverflow.com/questions/46614526/how-to-import-a-csv-file-into-a-data-array

#  Title: How to modify ttk Combobox fonts?
#  Author: NirMH
#  Date Posted: Mar 29, 17 
#  Availability: https://stackoverflow.com/questions/43086378/how-to-modify-ttk-combobox-fonts

#  Title: Python OpenCV - show an image in a Tkinter window
#  Author: Paul Joshi
#  Date Posted: April 20, 2018
#  Availability:https://solarianprogrammer.com/2018/04/20/python-opencv-show-image-tkinter-window/

#  Title: Python os.write() Method
#  Author: tutorialspoint
#  Availability:https://www.tutorialspoint.com/python/os_write.htm

#  Title: Python os.write() Method
#  Author: Paul D. Waite
#  Date Posted: April 26, 2017
#  Availability:https://stackoverflow.com/questions/8258432/days-between-two-dates

#  Title: An elegant way to run periodic tasks in python
#  Author:sankalp jonna
#  Date Posted: Oct 30, 2018
#  Availability:https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679

#  Title: Formatting date ticks using ConciseDateFormatter
#  Author: Matplotlib development team
#  Date Posted: N/A
#  Availability:https://matplotlib.org/3.1.0/gallery/ticks_and_spines/date_concise_formatter.html

#  Title: Adding data labels to linechart
#  Author: mgilbert
#  Date Posted: Sept 25 2017
#  Availability:https://stackoverflow.com/questions/46063077/adding-data-labels-to-linechart

#  Title: Tkinter Digital Clock (Python)
#  Author: vegaseat
#  Date Posted: N/A
#  Availability:https://www.daniweb.com/programming/software-development/code/216785/tkinter-digital-clock-python
############################################################################################################################

#Import important libraries/make sure that you have install all
import ARD_functions_GC as ard   #ARD_functions_GC has the major functions to connect to the arduino and get input values
import tkinter as tk        #Tkinter is a GUI platform from python
from tkinter import *       #Import all from tkinter
from time import strftime, gmtime  #Use to convert the title of the csv files to datetime object
import matplotlib.pyplot as plt    #Very very powerful tool to view datapoints
import matplotlib.colors as mcolors #Color used to style the chart
import threading #for scheduling
from threading import Timer #This is used to assign timers
from tkinter import font  #Font of the frames
import datetime  #Datetime to get real time updates
import time   #to manipulate time
import PIL   #install pip install pillow
from pandas import DataFrame #Powerful tool to analyze data from csv files
from PIL import ImageTk, Image,ImageDraw,ImageFont  #Pil to display images
import sys  #sys libray
from pathlib import Path  #file system paths
import pandas as pd   #install pip install pandas
import os  #os to manipulate the files on the current operating system
from tkinter import ttk  #ttk to manipulate styles
from tkinter import messagebox #popup message
import matplotlib   #powerful graphing tool
matplotlib.use("TkAgg")  #manipulate style of graphs
from matplotlib.figure import Figure #Manipulate figures 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  #Place figures in canvas
from pandas.plotting import register_matplotlib_converters  #Register matpotlib to pandas
import matplotlib.dates as mdates  #For date formatting purposes
from matplotlib.dates import AutoDateFormatter, AutoDateLocator

import numpy as np
register_matplotlib_converters()  #register matpotlib converters
from PyQt5.QtWidgets import QApplication, QWidget

WAIT_Hour = 3600  #60 mins of seconds
WAIT_Day=86400  #24 hours of seconds
Fast=1    #1/7 of seconds
Mb=1000000   #size of 1 MB is 1000000 bytes
global connectS
global mythread
global stop_threads
global allFiles
global selected
connectS = "N-CXN"

##########################################FUNCTIONS##############################################################################
#### Arduino Serial port
# Port in which Arduino is connected
com_arr = []*30 #array of ports
stop_threads = False

allFiles = np.asarray(ard.Files)
# for windows
com = 'COM3'
com_arr.append('COM13')
com_arr.append('COM3')
com_arr.append('COM4')
com_arr.append('COM7')
com_arr.append('COM11')
com_arr.append('COM12')
com_arr.append('COM14')
com_arr.append('COM15')
# for Raspberry PI
com_arr.append('/dev/ttyACM1')
com_arr.append('/dev/ttyACM2')
com_arr.append('/dev/ttyACM3')
com_arr.append('/dev/ttyUSB0')
com_arr.append('/dev/ttyUSB1')

#Thread class is called to create the thread and assign tasks to each one 
class MyThread(threading.Thread): #Each of the 
    def run(self):
        global A
        while True: #While loop to keep running the threads
            if ard.run :  #If the arduino is running check all counters at the same time and do debouncing
                value=int(self.getName()) #Get the current pinId       
                connectS="CXN"  #Set the connectS label to connection status
                ard.ReadSwitch(A,value)  #Read the inputs of the current pin Id
                index=value-22 #Get the index id of the current pin by substracting 22 which is the initial pin
                current=ard.ticks[index] #save the current tick read into a varriable

                if (current==0): #If the pin is driven to low, a tick has happened
                    print("Volume increased for Counter of pin ID:"+str(value)) #troubleshooting message for user
                    ard.volume[index]=ard.volume[index]+30 #Increase the volume for this particular counter
                    filePath=ard.folder+"\\"+allFiles[0][index] #If there is a tick, save to the right csv file
                    fd = open(filePath,'a')  #open the csv file that corresponds to the counter
                    col1=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"," #The current data
                    row=col1+str(ard.volume[index])+"\n"  #The date and the volume of that Gas counter
                    fd.write(row) #Write to the file
                    fd.flush()
                    fd.close()  #close the file
                    time.sleep(2.5) #debouncing to make sure that the pin output is not repeating
                    ard.ticks[index]=1 #set the pin output back to high
                if stop_threads: 
                    break
                time.sleep(0.02) #sleep a bit before starting reading process of same thread pin                        
            else:
                print("Port selected:" +com) #remind user of the com port name selected
                A = ard.ArdConnect(com) #retry another connection with arduino
                connectS="N-CXN" #update lable to no connection
                if ard.run: #if succeeded
                    ard.ArdSetup(A) #Setup arduino
                    connectS="CXN" #update label to connection

#main() function initialized all the threads through the thread class and passes the pin id
def main(): 
    global mythread #global thread object
    for x in range(30): #30 thread for 30 pins
        pinID=x+22; #Create the initial thread id associated with the pinId                                            
        mythread = MyThread(name = format(pinID))  #Create the thread
        mythread.start()  #Start the thread
        print("Thread for pin ID #"+str(pinID)+" created\n") #Tell user that the thread has been created
        time.sleep(1) #Sleep for one second before starting new thread            

#This function is called each time an hour passes, volume is reset for more presice data
#If the volume is not reset, the graph will always have a linear correlation and the user would have
#understanding on which hoour/day/month had more volume
def resetVolume(): 
    global threading2
    threading2 = Timer(WAIT_Hour, resetVolume)
    threading2.start() #Set timer for 60 mns
    for i in range(30):  #Reset the overall volume sums to 0 for the next hour
        ard.volume[i]=0 #for each counter

#This function is called each time a day passes, volume is reset for more presice data
def oneDay(): #This function is called each time a day passes, volume is reset, files are verified
    global threading3
    threading3=Timer(WAIT_Day, oneDay)#Set timer for 24 hrs
    threading3.start() #Set timer for 24 hrs
    today=datetime.datetime.now().date() #Get the current date
    for i in range(30):  #For 30 reactors
        ard.volume[i]=0  #reset the volume for each counter
        filePath=ard.folder+"\\"+allFiles[0][i] #filepath for each counter
        filep=allFiles[0][i].split(" ")  #split the title pf the string to get the date part
        passFile = datetime.datetime.strptime(filep[0], '%Y-%m-%d').date() #convert the string date to datetime object
        days=(today-passFile).days #calculate teh difference between file creation date and current date
        size=os.path.getsize(filePath) #Get the size of the file

        if(days>=30 or size>=(10*Mb)): #if 30 days has passed or the file size is 10 MB, delete the file and create a new one
            allFiles[0][i]=str(today)+" - GC"+str(i+1)+".csv" #update the title to today's date
            filePath=ard.folder+"\\"+allFiles[0][i] #get the new file path
            fd = open(filePath,'a') #create the new file
            firstRow = "Date-Time,Volume\n" #create first line to file or in our case first two columns
            fd.write(firstRow) #Write first line to file
            fd.flush()
            fd.close() #close the file

################################################ Main CODE Brain #####################################################
global A #global Arduino object
print("Port selected:" +com) #Tell user the com port selected
flagRun=False

while(flagRun==False):
    A = ard.ArdConnect(com) #Connect to the arduino
    print("Port selected:" +com)
    time.sleep(1)
    if(ard.run):
        flagRun=True

ard.ArdSetup(A) #Setup pins
print(A) #Print arduino object


resetVolume() #start the volume reset timer
oneDay() #check if 30 days has passes, reset the volume, check size of file
main() #main() initializes threads for each pins

#deleteChildren function destroys previous canvas to prevent code from crashing
def deleteChildren():
    for child in GUI_window.winfo_children():
        if (child !=GUI_LeftPanelLeftBar):
            child.destroy()

#Each time a use selects a different counter
def selection_changed(event): #Get the selection from the combobox
    selected=counterMenu.current() #Get the index of the selected Gas counter
    ### Create default Graph Frame
    deleteChildren()

    GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')  #graph window
    GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 11*(h//10)) #window size

    # Header label
    GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=counterMenu.get()+' - Graph', 
        font=("Calibri", int(15*zl), "bold"), bg="white") 

    GUI_GraphHeaderLabel.place(x=int(w*0.20), y=int(h*0.034)) #place label in window
    figure = Figure(figsize=(7, 7), dpi=100) #create default figure
    plot = figure.add_subplot(1, 1, 1) #only requires one figure
    canvas = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas) #place the figure in a canvas
    canvas.get_tk_widget().grid(rowspan=50, sticky="nesw",padx=int(w*0.124),pady=int(h*0.08)) #place a grid for the canvas

    GUI_24HourButton= tk.Button(GUI_GraphicsCanvas, text= "Hour Rate" , bg= 'white', 
        command=lambda :HourRate(selected), font=("Calibri", int(12*zl)))  #create a 24 hour button
    GUI_24HourButton.place(x=int(w*0.54), y=int(h*0.17) , relwidth= 0.18, relheight=0.10)  #place the button in the graph window

    GUI_WeekButton= tk.Button(GUI_GraphicsCanvas, text= "Week Rate" , bg= 'white', 
        command=lambda :WeekRate(selected),font=("Calibri", int(12*zl)))  #create a week button 
    GUI_WeekButton.place(x=int(w*0.54), y=int(h*0.26) , relwidth= 0.18, relheight=0.10)  #place the week button in the graph window

    GUI_MonthButton= tk.Button(GUI_GraphicsCanvas, text= "Month Rate" , bg= 'white',
        command=lambda :MonthRate(selected), font=("Calibri", int(12*zl)))  #create a month button  
    GUI_MonthButton.place(x=int(w*0.54), y=int(h*0.35) , relwidth= 0.18, relheight=0.10)  #place the month button in the graph window

   

def homePage():#Information page
    deleteChildren()

    GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='indianred')
    GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 11*(h//10))
    
    #A few lines of information about the project
    text='Welcome to our Gui for Gas Counter!\n There are 30 Gas Counters available in the list.\n'
    text=text+'The flow rate for each counter is displayed as chart and is selectable between m-1, h-1, d-1.\n'
    text=text+'All rates are saved in a csv file.\n'
    text=text+'You will be able to view the data as well with the view data button.\n\n\n'
    text=text+'We hope that you will have a good time analyzing the rates.'

    GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=text,bg="indianred",
        fg="white", justify='center',font=("Calibri", int(14*zl), "bold"), anchor='n') #Label for the header
    GUI_GraphHeaderLabel.place(x=int(w*0.032), y=int(h*0.14)) #Label for the information page

def HourRate(index): #Resamples the data based on hours
    rateType="Hour Rate" #Title of the graph
    now=datetime.datetime.now() #get today's date
    desiredRange=datetime.timedelta(hours=1) #obtain date for last 24 hrs
    dayRange=now-desiredRange  #Get the date

    FullData = pd.read_csv(ard.folder+"\\"+allFiles[0][index], index_col=0) #Fetch the csv file for the selected counter
    FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S') #set the first column to datetime
    toPlot=FullData.loc[str(dayRange) : str(now)] #Select the data based on that
    newHour=toPlot.resample('5min').sum()  #Resample the data based on hours and sum the data for each hour
    graphIt(300, newHour, index, rateType,0) #Send everything to the graphIt function

def WeekRate(index): #Resamples the data based on the last 7 days
    rateType="Week Rate" #Title of the graph
    now=datetime.datetime.now() #get today's date
    desiredRange=datetime.timedelta(days=7) #obtain date for last 7 days including today
    WeekRange=now-desiredRange #Get the date

    FullData = pd.read_csv(ard.folder+"\\"+allFiles[0][index], index_col=0) #Fetch the csv file for the selected counter
    FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S') #set the first column to datetime
    toPlot=FullData.loc[str(WeekRange) : str(now)] #Select the data based on that
    new_Week=toPlot.resample('D').sum()  #Resample the data based on days and sum the data for the last 7 days
    graphIt(8, new_Week, index, rateType,1) #Send everything to the graphIt function


def MonthRate(index): #Resamples the data based on the last 30 days
    rateType="Month Rate" #Title of the graph
    now=datetime.datetime.now()  #get today's date
    desiredRange=datetime.timedelta(days=31) #obtain date for last 30 days including today
    MonthRange=now-desiredRange #Get the date
    FullData = pd.read_csv(ard.folder+"\\"+allFiles[0][index], index_col=0) #Fetch the csv file for the selected counter
    FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S') #set the first column to datetime
    toPlot=FullData.loc[str(MonthRange) : str(now)] #Select the data based on that
    new_Month=toPlot.resample('D').sum() #Resample the data based on days and sum the data for the last 30 days
    graphIt(32, new_Month, index,rateType,2) #Send everything to the graphIt function


def graphIt(days, data, index,rateType,gtype): #This function graphs the data based on selected counter
    #This arrays formats the x axis, according to time or dates
    deleteChildren()

    GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white') #canvas to hold the graph
    GUI_GraphicsCanvas.place(x= int(w*0.202),y=0  ,width= 8*(w//10) , height= 9*(h//10)) #size and position of canvas

    GUI_24HourButton= tk.Button(GUI_GraphicsCanvas, text= "Hour Rate" , bg= 'white', 
    command=lambda :HourRate(index), font=("Calibri", int(12*zl)))  #Button to access last 24 hours graph
    GUI_24HourButton.place(x=int(w*0.64), y=int(h*0.208) , relwidth= 0.16, relheight=0.10) #Size and position of button

    GUI_WeekButton= tk.Button(GUI_GraphicsCanvas, text= "Week Rate" , bg= 'white', 
    command=lambda :WeekRate(index),font=("Calibri", int(12*zl))) #Button to access last 7 days graph
    GUI_WeekButton.place(x=int(w*0.64), y=int(h*0.297) , relwidth= 0.16, relheight=0.10) #Size and position of button

    GUI_MonthButton= tk.Button(GUI_GraphicsCanvas, text= "Month Rate" , bg= 'white',
    command=lambda :MonthRate(index), font=("Calibri", int(12*zl))) #Button to access last 30 days graph
    GUI_MonthButton.place(x=int(w*0.64), y=int(h*0.386) , relwidth= 0.16, relheight=0.10) #Size and position of button

   
    today=datetime.datetime.now().strftime("%Y-%m-%d")

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    formatter.formats = ['%y',  # ticks are mostly years
                         '%b',       # ticks are mostly months
                         '%d',       # ticks are mostly days
                         '%H:%M',    # hrs
                         '%H:%M',    # min
                         '%S.%f', ]  # secs
    # these are mostly just the level above...
    formatter.zero_formats = [''] + formatter.formats[:-1]
    # ...except for ticks that are mostly hours, then it is nice to have
    # month-day:
    formatter.zero_formats[3] = '%d-%b'
    formatter.offset_formats = ['',
                                '%Y',
                                '%b %Y',
                                '%d %b %Y',
                                '%d %b %Y',
                                '%d %b %Y %H:%M', ]
    if(len(data)<=days and len(data)!=0): #Check the length of data
        header=rateType+" for Gas Counter "+str(index+1) #header of page
        GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=header,  fg="firebrick",bg='white',  
            font=("Calibri", int(18*zl), "bold"), anchor='n') #place header
        GUI_GraphHeaderLabel.place(x=int(w*0.17),y=(h*0.069))

        figure = plt.Figure(figsize=(14,16), dpi=100) #figure to hold plot
        ax = figure.add_subplot(111) #we only need one plot
        line = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas) #we have a line graph
        line.get_tk_widget().place(x=int(w*0.0014),y=int(h*0.116), relwidth=0.80, relheight=0.85) #Place the line graph
        ax.plot(data,marker='o', markersize=8, linestyle='-', label=rateType+' Resample', color='red',clip_on=False) #plot the data
        ax.set_ylabel('Volume (ml)',size=14) #set the y axis label
        ax.margins(0.05)

        ax.grid(True) #Place grid on the graph plot

        for i,j in data.Volume.items(): #anotate the points on the graph
            ax.annotate(str(j), xy=(i, j),size=14) #place in x,y axis

        if(gtype==0): #gas type graph for 24 hours  
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            ax.tick_params(direction='out', length=15, width=1)
            ax.margins(0.05)
            ax.set_xlabel('Last hour',size=14) #set the y axis label
            GUI_24HourButton.configure(bg='firebrick',fg='white',relief=SUNKEN)

        if(gtype==1): #gas type graph for last 7 days
            desiredRange=datetime.timedelta(days=7)
            week=(datetime.datetime.now()-desiredRange).strftime("%Y-%m-%d")
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            ax.tick_params(direction='out', length=7, width=1)
            ax.set_xlim(week,today)
            ax.margins(x=3)
            ax.set_xlabel('Last 7 days',size=14) #set the y axis label
            GUI_WeekButton.configure(bg='firebrick',fg='white',relief=GROOVE)

        if(gtype==2): #gas type graph for last 30 days
            desiredRange=datetime.timedelta(days=30)
            month=(datetime.datetime.now()-desiredRange).strftime("%Y-%m-%d")
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            ax.set_xlim(month,today)
            ax.margins(x=3)
            ax.set_xlabel('Last 30 days',size=14) #set the x axis label
            GUI_MonthButton.configure(bg='firebrick',fg='white', relief=GROOVE)

    else: #If the length of the data is equal to 0
        header="Not enough data to graph the "+ rateType+" for Gas Counter "+str(index+1)+"\nTry again later or pick another option"
        GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=header,  fg="black",bg='white',  
            font=("Calibri", int(14*zl), "bold"), anchor='n') #style label
        GUI_GraphHeaderLabel.place(x=int(w*0.117),y=int(h*0.011)) #place label
        figure = Figure(figsize=(8, 6), dpi=100) #create figure
        plot = figure.add_subplot(1, 1, 1) #plot dummy graph
        canvas = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas) #creat canvas and place figure in canvas
        canvas.get_tk_widget().grid(rowspan=50, sticky="nesw",padx=int(w*0.104),pady=int(h*0.10)) #place canvas in grid

def _SerialPortChange():
    global com
    com = GUI_SerialPortValue.get()
    return True

## Main window size and zoom(temporary)
z=1         # ZOOM
zl=1.6  *z  # Font zoom


GUI_window = tk.Tk() #Main window

sw, sh = GUI_window.winfo_screenwidth(), GUI_window.winfo_screenheight() #height of window based on the computer size
w = int(sw*z)
h = int(sh*z)

x =(sw/2) -(w/2)
y =(sh/2) -(h/2)


bigfont = font.Font(family="Helvetica",size=12) # Set font of the entire window
GUI_window.option_add("*TCombobox*Listbox*Font", bigfont) #Add font to the combo-box
GUI_window.geometry('{}x{}'.format(w ,h,0,0)) #set height and width of GUI window


if (os.name=='nt'):
    GUI_window.state('zoomed')
if (os.name=='posix'):
    GUI_window.attributes('-zoomed',True)

GUI_window.configure(bg='white') #background white
GUI_window.resizable(0,0) #do not allow resize because it messes the ratio


GUI_LeftPanelLeftBar = tk.Canvas(GUI_window, bg="firebrick" ) #Left panel holds menu
GUI_LeftPanelLeftBar.place(x=0,y=0 ,height= h, width=(w*0.2) ) #Place panel

#From line 362 to line 378 was obtain from web source (view references for digital clock with tkinter)
time1 = ''
clock = Label(GUI_LeftPanelLeftBar, font=('times', 16, 'bold'), bg='firebrick',fg="white")
clock.pack(fill=BOTH, expand=1) #pack the clock
clock.place(x=w*0.017,y=w*0.0065) #placement
def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%A, %B %e %Y\nTime: %H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)

tick() #create function

RGB_Graph_b1 =  '#{:02X}{:02X}{:02X}'.format(181,197,196)
Info_Button= tk.Button(GUI_LeftPanelLeftBar, text= "Info" , command=homePage,fg='firebrick',
 bg="white",font=("Calibri", int(11*zl),"bold")) #create info button
Info_Button.place(x=int(w*0.045), y=int(h*0.09) , relwidth= 0.49, relheight=0.04) #Place info button in window

GUI_GraphHeaderLabel=tk.Label(GUI_LeftPanelLeftBar, text='Select a Counter',bg="firebrick",
    fg="white", font=("times", int(14*zl), "bold"), anchor='n') #style and create label
GUI_GraphHeaderLabel.place(x=int(w*0.022), y=int(h*0.16)) #Place label in left bar
counterMenu = ttk.Combobox(GUI_LeftPanelLeftBar, state = "readonly") #COMBO-BOX menu
counterMenu[ "values" ] =ard.Counters #Set the values of the menu
counterMenu.config(width=int(w*0.016),height=int(h*0.046), background="red",font=int(20*zl),justify="center") #configurate
counterMenu.place(x=int(w*0.004), y=int(h*0.208))#place on window
counterMenu.bind( "<<ComboboxSelected>>" ,selection_changed ) #on select, call function

GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white') #create canvas
GUI_GraphicsCanvas.place(x= int(w*0.202) ,y=0  ,width= 8*(w//10) , height= 11*(h//10)) #style canvas

############# Status Bar #########################################################

GUI_SerialPortLabel = tk.Label(GUI_LeftPanelLeftBar,text='PORT',bg="firebrick",fg="white", font=("times", int(11*zl), "bold"), anchor='n')
GUI_SerialPortLabel.place(x=int(w*0.004),y=int(h*0.92), width=int(w*0.05),height=int(h*0.046))
#
GUI_SerialPortValue = tk.Spinbox(GUI_LeftPanelLeftBar, values=com_arr, bg= 'white', font= 10, command= _SerialPortChange)
GUI_SerialPortValue.place(x=int(w*0.055),y=int(h*0.92), relwidth= 1-0.7, height=int(h*0.040))
# #ARDUINO STATUSd
GUI_StatusInfo=tk.Label(GUI_LeftPanelLeftBar,bg= 'firebrick',anchor='e',text=connectS,fg="white",font=("times", int(11*zl), "bold"))
GUI_StatusInfo.place(x=int(w*0.12),y=int(h*0.92), width=int(w*0.05),height=int(h*0.046))
##################################################################################
path = "image.png" #dummy image for intro
img = ImageTk.PhotoImage(Image.open(path)) #fetch image
panel = tk.Label(GUI_GraphicsCanvas, image = img) #place a label
panel.pack(side = "bottom", fill = "both", expand = "yes") #pack overall

#The program will not work without this loops
GUI_window.mainloop() #keep the program in a continuous loop
threading2.cancel()
threading3.cancel()
stop_threads = True
mythread.join()
sys.exit()                  
                                            
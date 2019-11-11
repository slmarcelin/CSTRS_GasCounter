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
#  version :3.1

#  Title: Adding data labels to linechart
#  Author: mgilbert
#  Date Posted: Sept 25 2017
#  Availability:https://stackoverflow.com/questions/46063077/adding-data-labels-to-linechart
#  version :3.1
############################################################################################################################

#Import important libraries/make sure that you have install all
import ARD_funct_2 as ard   #ArD_funct_2 has the major functions to connect to the arduino and get input values
import tkinter as tk        #Tkinter is a GUI platform from python
from tkinter import *       #Import all from tkinter
from threading import Timer #This is used to assign timers
from time import strftime, gmtime  #Use to convert the title of the csv files to datetime object
import matplotlib.pyplot as plt    #Very very powerful tool to view datapoints
import matplotlib.colors as mcolors #Color used to style the chart
from tkinter import font  #Font of the frames
import datetime  #Datetime to get real time updates
import time   #to manipulate time
import threading #for scheduling
import PIL   #install pip install pillow
from pandas import DataFrame #Powerful tool to analyze data from csv files
from PIL import ImageTk, Image,ImageDraw,ImageFont  #Pil to display images
import sys  #sys libray
from pathlib import Path  #file system paths
import pandas as pd   #install pip install pandas
import os  #os to maniulate the files on the current operating system
from tkinter import ttk  #ttk to manipulate styles
import matplotlib   #powerful graphing tool
matplotlib.use("TkAgg")  #manipulate style of graphs
from matplotlib.figure import Figure #Manipulate figures 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  #Place figures in canvas
from pandas.plotting import register_matplotlib_converters  #Register matpotlib to pandas
import matplotlib.dates as mdates  #For date formatting purposes

register_matplotlib_converters()  #register matpotlib converters

WAIT_Hour = 3600  #60 mins of seconds
WAIT_Day=86400  #24 hours of seconds
Fast=0.25    #1/4 of seconds


def getInput():  #Get input from the Gas counter every 0.25 seconds
	threading.Timer(Fast, resetVolume).start()  #Set the timer
	if ard.run :  #If the arduino is running
		ard.ReadSwitch()  #Read the inputs
		for i in range(30):  #we have 30 inputs fron 30 gas Counters
			if(ard.ticks[i]==1): #ticks array holds reed switch values for each counter
				volume[i]=volume[i]+30 #Increase the volume for this particular counter
				filePath=ard.folder+"\\"+ard.Files[0][i] #If there is a tick, save to the right csv file
				fd = os.open(filePath,os.O_RDWR)  #open the csv file that corresponds to the counter
				col1=str(datetime.datetime.now())+"," #The current date
				row=col1+sr(volume[i])  #The date and the volume of that Gas counter
				os.write(fd,str.encode(row)) #Write to the file
				os.close(fd)  #close the file



def resetVolume(): #This function is called each time an hour passes, volume is reset for more presice data
    threading.Timer(WAIT_Hour, resetVolume).start() #Set timer for 60 mns
    for i in range(30):  #Reset the overall volume sums to 0 for the next hour
    	ard.volume[i]=0 #for each counter


def oneDay(): #This function is called each time a day passes, volume is reset, files are verified
    threading.Timer(WAIT_Day, oneDay).start() #Set timer for 24 hrs
    today=datetime.datetime.now().date() #Get the current date
    for i in range(30):  #For 30 reactors
    	ard.volume[i]=0  #reset the volume for each counter
    	filePath=ard.folder+"\\"+ard.Files[0][i] #filepath for each counter
    	filep=ard.Files[0][i].split(" ")  #split the title pf the string to get the date part
    	passFile = datetime.datetime.strptime(filep[0], '%Y-%m-%d').date() #convert the string date to datetime object
    	days=(today-passFile).days #calculate teh difference between file creation date and current date
    	size=os.path.getsize(ard.folder+"\\"+ard.Files[0][i]) #Get the size of the file
    	if(days==30 or size==1000000): #if 30 days has passed or the file size is 10 MB, delete the file and create a new one
    		os.remove(ard.folder+"\\"+ard.Files[0][i]); #remove the file
    		ard.Files[0][i]=str(today)+" - GC"+i+".csv" #create a new title
    		filePath=ard.folder+"\\"+ard.Filesp[0][i] #get the file path
    		open(filePath, 'a').close() #create the new file in the folder and close it



getInput() #start the input retriever timer
resetVolume() #start the volume reset timer
oneDay() #check if 30 days has passes, reset the volume, check size of file

def selection_changed(event): #Get the selection from the combobox
	selected=counterMenu.current() #Get the index of the selected Gas counter

	### Create default Graph Frame
	GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')  #graph window
	GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10)) #window size

	# Header label
	GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=counterMenu.get()+' - Graph', 
		font=("Calibri", int(15*zl), "bold"), bg="white") 

	GUI_GraphHeaderLabel.place(x=420, y=30) #place label in window
	figure = Figure(figsize=(7, 7), dpi=100) #create default figure
	plot = figure.add_subplot(1, 1, 1) #only requires one figure
	canvas = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas) #place the figure in a canvas
	canvas.get_tk_widget().grid(column=2, row=780, rowspan=50, sticky="nesw",padx=190,pady=70) #place a grid for the canvas

	GUI_24HourButton= tk.Button(GUI_GraphicsCanvas, text= "Hour Rate" , bg= 'white', 
		command=lambda :HourRate(selected), font=("Calibri", int(12*zl)))  #create a 24 hour button
	GUI_24HourButton.place(x=830, y=150 , relwidth= 0.18, relheight=0.10)  #place the button in the graph window

	GUI_WeekButton= tk.Button(GUI_GraphicsCanvas, text= "Week Rate" , bg= 'white', 
		command=lambda :WeekRate(selected),font=("Calibri", int(12*zl)))  #create a week button 
	GUI_WeekButton.place(x=830, y=227 , relwidth= 0.18, relheight=0.10)  #place the week button in the graph window

	GUI_MonthButton= tk.Button(GUI_GraphicsCanvas, text= "Month Rate" , bg= 'white',
		command=lambda :MonthRate(selected), font=("Calibri", int(12*zl)))  #create a month button  
	GUI_MonthButton.place(x=830, y=304 , relwidth= 0.18, relheight=0.10)  #place the month button in the graph window


def homePage(): #the Homepage is not working yet
	GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='indianred')
	GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))

	text='Welcome to our Gui for Gas Counter!\n There are 30 Gas Counters available in the list.\n'
	text=text+'The flow rate for each counter is displayed as chart and is selectable between m-1, h-1, d-1.\n'
	text=text+'The rates are also saved in a csv file.\n\n\n'
	text=text+'We hope that you will have a good time analyzing the rates.'

	GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=text,bg="indianred",
		fg="white", justify='center',font=("Calibri", int(14*zl), "bold"), anchor='n')
	GUI_GraphHeaderLabel.place(x=50, y=120)

def HourRate(index):
	rateType="Hour Rate"
	now=datetime.datetime.now()
	desiredRange=datetime.timedelta(hours=24)
	dayRange=now-desiredRange
	FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][index], index_col=0)
	FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S')
	toPlot=FullData.loc[str(dayRange) : str(now)]
	newHour=toPlot.resample('H').sum()
	graphIt(25, newHour, index, rateType,0)

def WeekRate(index):
	rateType="Week Rate"
	now=datetime.datetime.now()
	desiredRange=datetime.timedelta(days=8)
	WeekRange=now-desiredRange

	FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][index], index_col=0)
	FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S')
	toPlot=FullData.loc[str(WeekRange) : str(now)]
	new_Week=toPlot.resample('D').sum()
	graphIt(8, new_Week, index, rateType,1)


def MonthRate(index):
	rateType="Month Rate"
	now=datetime.datetime.now()
	desiredRange=datetime.timedelta(days=31)
	MonthRange=now-desiredRange
	FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][index], index_col=0)
	FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S')
	toPlot=FullData.loc[str(MonthRange) : str(now)]
	new_Month=toPlot.resample('D').sum()
	graphIt(31, new_Month, index,rateType,2)

def graphIt(days, data, index,rateType,gtype):

	#This arrays formats the x axis, according to time or dates
	locator = mdates.AutoDateLocator()
	formatter = mdates.ConciseDateFormatter(locator)
	formatter.formats = ['%y','%b','%d','%H:%M','%H:%M','%S.%f',]     
	formatter.zero_formats = [''] + formatter.formats[:-1]
	formatter.zero_formats[3] = '%d-%b'
	formatter.offset_formats = ['','%Y','%b %Y','%d %b %Y','%d %b %Y','%d %b %Y %H:%M', ]

	GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')
	GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))

	GUI_24HourButton= tk.Button(GUI_GraphicsCanvas, text= "Hour Rate" , bg= 'white', 
		command=lambda :HourRate(index), font=("Calibri", int(12*zl))) 

	GUI_24HourButton.place(x=984, y=180 , relwidth= 0.16, relheight=0.10)

	GUI_WeekButton= tk.Button(GUI_GraphicsCanvas, text= "Week Rate" , bg= 'white', 
		command=lambda :WeekRate(index),font=("Calibri", int(12*zl))) 
	GUI_WeekButton.place(x=984, y=257 , relwidth= 0.16, relheight=0.10)

	GUI_MonthButton= tk.Button(GUI_GraphicsCanvas, text= "Month Rate" , bg= 'white',
		command=lambda :MonthRate(index), font=("Calibri", int(12*zl))) 

	GUI_MonthButton.place(x=984, y=334 , relwidth= 0.16, relheight=0.10)

    
	if(len(data)<=days):
		header=rateType+" for Gas Counter "+str(index+1)
		GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=header,  fg="black",bg='white',  
			font=("Calibri", int(18*zl), "bold"), anchor='n')

		GUI_GraphHeaderLabel.place(x=270,y=60)
		figure = plt.Figure(figsize=(15,15), dpi=100)
		ax = figure.add_subplot(111)
		line = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas)
		line.get_tk_widget().place(x=1,y=100, relwidth=0.80, relheight=0.85)
		ax.plot(data,marker='o', markersize=8, linestyle='-', label=rateType+' Resample', color='red')
		ax.set_ylabel('Volume (ml)',size=14)
		ax.xaxis.set_major_locator(locator)
		ax.xaxis.set_major_formatter(formatter)

		if(gtype==0):
			 ax.set_xlabel('Last 24 Hours',size=14)
		if(gtype==1):
			 ax.set_xlabel('Last 7 days',size=14)
		if(gtype==2):
			 ax.set_xlabel('Last 30 days',size=14)	

		for i,j in data.Volume.items():
		    ax.annotate(str(j), xy=(i, j),size=14)
	else:
		header="Not enough data to graph the "+ rateType+" for Gas Counter "+str(index+1)+"\nTry again later or pick another option"
		GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=header,  fg="black",bg='white',  
			font=("Calibri", int(14*zl), "bold"), anchor='n')
		GUI_GraphHeaderLabel.place(x=180,y=10)
		figure = Figure(figsize=(8, 6), dpi=100)
		plot = figure.add_subplot(1, 1, 1)
		canvas = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas)
		canvas.get_tk_widget().grid(column=2, row=780, rowspan=50, sticky="nesw",padx=160,pady=90)

######################################################
##Start the Program ##################################################################
# global A
# A = ard.ArdConnect(com)
# ard.ArdSetup(A)

#### Arduino Serial port
# Port in which Arduino is connected
com_arr = []*30 #array of ports
# for windows
com_arr.append('COM3')
com_arr.append('COM4')
com_arr.append('COM7')
com_arr.append('COM11')
com_arr.append('COM12')
com_arr.append('COM13')
com_arr.append('COM14')
com_arr.append('COM15')
# for Raspberry PI
com_arr.append('/dev/ttyACM1')
com_arr.append('/dev/ttyACM2')
com_arr.append('/dev/ttyACM3')
com_arr.append('/dev/ttyUSB0')
com_arr.append('/dev/ttyUSB1')


## Main window size and zoom(temporary)
z=1         # ZOOM
zl=1.6  *z  # Font zoom

## Main Window
GUI_window = tk.Tk()
w, h = GUI_window.winfo_screenwidth(), GUI_window.winfo_screenheight()
bigfont = font.Font(family="Helvetica",size=12)
GUI_window.option_add("*TCombobox*Listbox*Font", bigfont)
## Main window size and zoom(temporary)
z=1         # ZOOM
zl=1.6  *z  # Font zoom

GUI_window.geometry('{}x{}'.format(int(w*0.5) , int(h*0.5)) )
GUI_window.state("zoomed")
GUI_window.configure(bg='white')
GUI_window.resizable(1,1)

#GUI_LeftPanelLeftBar.pack(side=LEFT)
GUI_LeftPanelLeftBar = tk.Canvas(GUI_window, bg="firebrick" )
GUI_LeftPanelLeftBar.place(x=0,y=0 ,height= h, width=(w*0.2) )
selectedCounter=StringVar()


time1 = ''
clock = Label(GUI_LeftPanelLeftBar, font=('times', 16, 'bold'), bg='firebrick',fg="white")
clock.pack(fill=BOTH, expand=1)
clock.place(x=15,y=10)
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
tick()
# Hour button

Home_Button= tk.Button(GUI_LeftPanelLeftBar, text= "Info" , command=homePage,fg='firebrick',
 bg="white",font=("Calibri", int(11*zl),"bold")) 
Home_Button.place(x=70, y=80 , relwidth= 0.49, relheight=0.04)

GUI_GraphHeaderLabel=tk.Label(GUI_LeftPanelLeftBar, text='Select a Counter',bg="firebrick",
	fg="white", font=("times", int(14*zl), "bold"), anchor='n')
GUI_GraphHeaderLabel.place(x=35, y=140)

counterMenu = ttk.Combobox(GUI_LeftPanelLeftBar, state = "readonly")
counterMenu[ "values" ] =ard.Counters
counterMenu.config(width=30,height=40, background="red",font=int(20*zl),justify="center")
counterMenu.place(x=7, y=180)
counterMenu.bind( "<<ComboboxSelected>>" ,selection_changed )




GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')
GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))

path = "image.png"
# img = Image.open(r'image.png')  
# draw = ImageDraw.Draw(img)  
# font = ImageFont.truetype(r'arial.ttf',24)  
# text = 'Welcome to the CSTR GUI\nPlease Select a Gas Counter to view graph rates'
# draw.text((200, 5), text, font = font, align ="center",fill ="black") 
# img=img.save('image.png')
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(GUI_GraphicsCanvas, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")



GUI_window.mainloop()

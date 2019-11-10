
import ARD_funct_2 as ard
#from tkinter.ttk import *
import tkinter as tk
from tkinter import *
from threading import Timer
from functools import partial
from time import strftime, gmtime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
#import random
from tkinter import font
import datetime
import time
import threading
import PIL
from pandas import DataFrame
from PIL import ImageTk, Image,ImageDraw,ImageFont 
import sys
from pathlib import Path
import pandas as pd
import os
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
WAIT_Hour = 3600
WAIT_Day=86400
Fast=0.25

def getInput():
	threading.Timer(Fast, resetVolume).start()
	if ard.run :
		ard.ReadSwitch()
		for i in range(30):
			if(ard.ticks[i]==1):
				volume[i]=volume[i]+30
				filePath=ard.folder+"\\"+ard.Files[0][i]
				fd = os.open(filePath,os.O_RDWR)
				col1=str(datetime.datetime.now())+","
				row=col1+sr(volume[i])
				os.write(fd,str.encode(row))
				os.close(fd)


#This function is called each time an hour passes, volume is reset
def resetVolume():
    threading.Timer(WAIT_Hour, resetVolume).start()
    for i in range(30):
    	ard.volume[i]=0

#This function is called each time a day passes, volume is reset, files are verified
def oneDay():
    threading.Timer(WAIT_Day, oneDay).start()	
    today=datetime.datetime.now().date()
    for i in range(30):
    	ard.volume[i]=0
    	filePath=ard.folder+"\\"+ard.Files[0][i]
    	filep=ard.Files[0][i].split(" ")
    	passFile = datetime.datetime.strptime(filep[0], '%Y-%m-%d').date()
    	days=(today-passFile).days
    	size=os.path.getsize(ard.folder+"\\"+ard.Files[0][i])
    	if(days==30 or size==1000000):
    		os.remove(ard.folder+"\\"+ard.Files[0][i]);
    		ard.Files[0][i]=str(today)+" - GC"+i+".csv"
    		filePath=ard.folder+"\\"+ard.Filesp[0][i]
    		open(filePath, 'a').close()



getInput()
resetVolume()
oneDay()

def selection_changed(event):
	# print("Selected "+str(counterMenu.current()))
	selected=counterMenu.current()
	### Update Graphs Frame
	GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')
	GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))
	# Header label
	GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=counterMenu.get()+' - Graph', font=("Calibri", int(15*zl), "bold"), bg="white")
	GUI_GraphHeaderLabel.place(x=420, y=30)
	figure = Figure(figsize=(7, 7), dpi=100)
	plot = figure.add_subplot(1, 1, 1)
	canvas = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas)
	canvas.get_tk_widget().grid(column=2, row=780, rowspan=50, sticky="nesw",padx=190,pady=70)

	GUI_24HourButton= tk.Button(GUI_GraphicsCanvas, text= "Hour Rate" , bg= 'white', command=lambda :HourRate(selected), font=("Calibri", int(12*zl))) 
	GUI_24HourButton.place(x=830, y=150 , relwidth= 0.18, relheight=0.10)

	GUI_WeekButton= tk.Button(GUI_GraphicsCanvas, text= "Week Rate" , bg= 'white', command=lambda :WeekRate(selected),font=("Calibri", int(12*zl))) 
	GUI_WeekButton.place(x=830, y=227 , relwidth= 0.18, relheight=0.10)

	GUI_MonthButton= tk.Button(GUI_GraphicsCanvas, text= "Month Rate" , bg= 'white',command=lambda :MonthRate(selected), font=("Calibri", int(12*zl))) 
	GUI_MonthButton.place(x=830, y=304 , relwidth= 0.18, relheight=0.10)

def homePage():
	GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')
	GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))
	GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text='Select a Counter',bg="firebrick",fg="white", font=("Calibri", int(18*zl), "bold"), anchor='n')
	GUI_GraphHeaderLabel.place(x=20, y=50)
	path = "image.png"
	img = ImageTk.PhotoImage(Image.open(path))
	panel = tk.Label(GUI_GraphicsCanvas, image = img)
	panel.pack(side = "bottom", fill = "both", expand = "yes")

def HourRate(index):
	rateType="Hour Rate"
	now=datetime.datetime.now()
	desiredRange=datetime.timedelta(hours=24)
	dayRange=now-desiredRange
	FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][index], index_col=0)
	FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S')
	toPlot=FullData.loc[str(dayRange) : str(now)]
	toPlot.resample('D').sum()
	graphIt(1, toPlot, index, rateType)

def WeekRate(index):
	rateType="Week Rate"
	now=datetime.datetime.now()
	desiredRange=datetime.timedelta(days=8)
	WeekRange=now-desiredRange

	FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][index], index_col=0)
	FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S')
	toPlot=FullData.loc[str(WeekRange) : str(now)]
	toPlot.resample('D').sum()
	graphIt(8, toPlot, index, rateType)


def MonthRate(index):
	rateType="Month Rate"
	now=datetime.datetime.now()
	desiredRange=datetime.timedelta(days=32)
	MonthRange=now-desiredRange
	FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][index], index_col=0)
	FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S')
	toPlot=FullData.loc[str(MonthRange) : str(now)]
	graphIt(32, toPlot, index,rateType)

def graphIt(days, data, index,rateType):
	GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')
	GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))

	GUI_24HourButton= tk.Button(GUI_GraphicsCanvas, text= "Hour Rate" , bg= 'white', command=lambda :HourRate(index), font=("Calibri", int(12*zl))) 
	GUI_24HourButton.place(x=984, y=180 , relwidth= 0.16, relheight=0.10)

	GUI_WeekButton= tk.Button(GUI_GraphicsCanvas, text= "Week Rate" , bg= 'white', command=lambda :WeekRate(index),font=("Calibri", int(12*zl))) 
	GUI_WeekButton.place(x=984, y=257 , relwidth= 0.16, relheight=0.10)

	GUI_MonthButton= tk.Button(GUI_GraphicsCanvas, text= "Month Rate" , bg= 'white',command=lambda :MonthRate(index), font=("Calibri", int(12*zl))) 
	GUI_MonthButton.place(x=984, y=334 , relwidth= 0.16, relheight=0.10)

    
	if(len(data)>=days):
		header=rateType+" for Gas Counter "+str(index+1)
		GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=header,  fg="black",bg='white',  font=("Calibri", int(18*zl), "bold"), anchor='n')
		GUI_GraphHeaderLabel.place(x=270,y=60)
		figure = plt.Figure(figsize=(15,15), dpi=100)
		ax = figure.add_subplot(111)
		line = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas)
		line.get_tk_widget().place(x=1,y=100, relwidth=0.80, relheight=0.85)
		data.plot(kind='line', legend=True, ax=ax, color='r',marker='.', fontsize=10)
	else:
		header="Not enough data to graph the "+ rateType+" for Gas Counter "+str(index+1)+"\nTry again later or pick another option"
		GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=header,  fg="black",bg='white',  font=("Calibri", int(14*zl), "bold"), anchor='n')
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

GUI_GraphHeaderLabel=tk.Label(GUI_LeftPanelLeftBar, text='Select a Counter',bg="firebrick",fg="white", font=("Calibri", int(18*zl), "bold"), anchor='n')
GUI_GraphHeaderLabel.place(x=20, y=50)

counterMenu = ttk.Combobox(GUI_LeftPanelLeftBar, state = "readonly")
counterMenu[ "values" ] =ard.Counters
counterMenu.config(width=31,height=40, background="red",font=int(20*zl),justify="center")
counterMenu.place(x=0, y=100)
counterMenu.bind( "<<ComboboxSelected>>" ,selection_changed )

# Hour button
Home_Button= tk.Button(GUI_LeftPanelLeftBar, text= "Home" , command=homePage,bg= 'white', font=("Calibri", int(12*zl))) 
Home_Button.place(x=70, y=10 , relwidth= 0.49, relheight=0.04)


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


import ARD_funct_2 as ard
#from tkinter.ttk import *
import tkinter as tk
from tkinter import *
from threading import Timer
from functools import partial
from time import strftime, gmtime
#import random
import datetime
import time
import threading
import sys
from pathlib import Path
import os

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
				filePath=ard.folder+"\\"+ard.Files[i]
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
    	filePath=ard.folder+"\\"+ard.Files[i]
    	filep=ard.Files[i].split(" ")
    	passFile = datetime.datetime.strptime(filep[0], '%Y-%m-%d').date()
    	days=(today-passFile).days
    	size=os.path.getsize(ard.folder+"\\"+ard.Files[i])
    	if(days==30 or size==1000000):
    		os.remove(ard.folder+"\\"+ard.Files[i]);
    		ard.Files[i]=str(today)+" - GC"+i+".csv"
    		filePath=ard.folder+"\\"+ard.Files[i]
    		open(filePath, 'a').close()



getInput()
resetVolume()
oneDay()

########################################################Start the Program ##################################################################
# global A
# A = ard.ArdConnect(com)
# ard.ArdSetup(A)

#### Arduino Serial port
# Port in which Arduino is connected
com_arr = [] #array of ports
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

GUI_window.mainloop()
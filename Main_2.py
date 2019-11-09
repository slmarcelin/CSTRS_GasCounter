
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
import datetime
import time
import threading
import PIL
from PIL import ImageTk, Image,ImageDraw,ImageFont 
import sys
from pathlib import Path
import os
from tkinter import ttk
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

def selection_changed(event):
	print("Selected "+counterMenu.get())
	### Update Graphs Frame
	GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')
	GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))
	# Header label
	GUI_GraphHeaderLabel=tk.Label(GUI_GraphicsCanvas, text=counterMenu.get()+' - Graph', font=("Calibri", int(15*zl), "bold"), bg="white")
	GUI_GraphHeaderLabel.place(x=480, y=10)
########################################################Start the Program ##################################################################
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

GUI_GraphHeaderLabel=tk.Label(GUI_LeftPanelLeftBar, text='Select a Counter',bg="firebrick",fg="white", font=("Calibri", int(20*zl), "bold"), anchor='n')
GUI_GraphHeaderLabel.place(x=5, y=40)

counterMenu = ttk.Combobox(GUI_LeftPanelLeftBar, state = "readonly")
counterMenu[ "values" ] =ard.Counters
counterMenu.config(width=26,height=40, background="red",font=34,justify="center")
counterMenu.place(x=0, y=100)
counterMenu.current(0)
counterMenu.bind( "<<ComboboxSelected>>" ,selection_changed )

GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')
GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))

path = "image.png"

img = Image.open(r'image.png')  
#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.

draw = ImageDraw.Draw(img)  
  
# specified font size 
font = ImageFont.truetype(r'arial.ttf',24)  
  
text = 'Welcome to the CSTR GUI\nPlease Select a Gas Counter to view graph rates'
# drawing text size 
draw.text((200, 5), text, font = font, align ="center",fill ="black") 
img=img.save('image.png')
img = ImageTk.PhotoImage(Image.open(path))
#The Pack geometry manager packs widgets in rows or columns.
panel = tk.Label(GUI_GraphicsCanvas, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
GUI_window.mainloop()
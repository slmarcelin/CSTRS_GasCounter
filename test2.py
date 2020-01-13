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
from tkinter import messagebox #popup message
import matplotlib   #powerful graphing tool
matplotlib.use("TkAgg")  #manipulate style of graphs
from matplotlib.figure import Figure #Manipulate figures 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  #Place figures in canvas
from pandas.plotting import register_matplotlib_converters  #Register matpotlib to pandas
import matplotlib.dates as mdates  #For date formatting purposes
from pandasgui import show
import numpy as np
register_matplotlib_converters()  #register matpotlib converters
from PyQt5.QtWidgets import QApplication, QWidget
WAIT_Hour = 3600  #60 mins of seconds
WAIT_Day=3000  #24 hours of seconds
Fast=0.25    #1/4 of seconds
here=30
for i in range(30):  #we have 30 inputs fron 30 gas Counters
	here=here+30 #Increase the volume for this particular counter
	filePath=ard.folder+"\\"+ard.Files[0][i] #If there is a tick, save to the right csv file
	fd = os.open(filePath,os.O_RDWR)  #open the csv file that corresponds to the counter
	col1=str(datetime.datetime.now())+"," #The current date
	row=col1+str(volume[i])  #The date and the volume of that Gas counter
	os.write(fd,str.encode(row)) #Write to the file
	os.close(fd)  #close the file

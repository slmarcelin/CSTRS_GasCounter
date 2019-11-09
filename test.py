
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

WAIT_SECONDS = 3

#For better reprensentations, reset the volume every day
def reset():
    threading.Timer(6, reset).start()
    print("I was here")

 #For better reprensentations, reset the volume every day
def here():
    threading.Timer(7, here).start()
    print("I am here now")

    
reset()   
here()




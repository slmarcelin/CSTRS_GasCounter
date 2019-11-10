import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
import ARD_funct_2 as ard
import datetime
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

now=datetime.datetime.now()
desiredRange=datetime.timedelta(hours=24)
dayRange=now-desiredRange

desiredRange=datetime.timedelta(days=8)
weekRange=now-desiredRange

desiredRange=datetime.timedelta(days=31)
MonthRange=now-desiredRange
# ard.folder+"\\"+ard.Files[0][0]
FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][0], index_col=0)
FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S') 
rangeg=FullData.loc[str(weekRange) : str(now)]

print(rangeg.resample('D').sum())
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
import ARD_funct_2 as ard
import datetime
import pandas as pd
GUI_window = tk.Tk()
w, h = GUI_window.winfo_screenwidth(), GUI_window.winfo_screenheight()


GUI_GraphicsCanvas= tk.Canvas(GUI_window, bg='white')
GUI_GraphicsCanvas.place(x= (w//10)+157 ,y=0  ,width= 8*(w//10) , height= 9*(h//10))
now=datetime.datetime.now()
desiredRange=datetime.timedelta(hours=24)
dayRange=now-desiredRange

desiredRange=datetime.timedelta(days=8)
weekRange=now-desiredRange

desiredRange=datetime.timedelta(days=31)
MonthRange=now-desiredRange
# ard.folder+"\\"+ard.Files[0][0]
FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][0], index_col=0)
FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S') 
rangeg=FullData.loc[str(weekRange) : str(now)]
rangeg.resample('D').sum()

figure = plt.Figure(figsize=(15,15), dpi=90)
ax = figure.add_subplot(111)
line = FigureCanvasTkAgg(figure, GUI_GraphicsCanvas)
line.get_tk_widget().place(x=0,y=100, relwidth=0.80, relheight=0.85)
ax.plot(rangeg,
marker='o', markersize=8, linestyle='-', label='Weekly Mean Resample')
GUI_window.mainloop()
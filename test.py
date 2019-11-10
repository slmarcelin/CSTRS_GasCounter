import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
import ARD_funct_2 as ard
import datetime
import pandas as pd


now=datetime.datetime.now()
desiredRange=datetime.timedelta(hours=24)
dayRange=now-desiredRange

desiredRange=datetime.timedelta(days=7)
weekRange=now-desiredRange

desiredRange=datetime.timedelta(days=31)
MonthRange=now-desiredRange
# ard.folder+"\\"+ard.Files[0][0]
FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][0], index_col=0)
FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S') 
rangeg=FullData.loc[str(weekRange) : str(now)]
print(len(rangeg))

print(rangeg.resample('4H').sum())

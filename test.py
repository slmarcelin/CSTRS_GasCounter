import pandas as pd
from pandasgui import show
import datetime
import ARD_funct_2 as ard
import platform  

now=datetime.datetime.now()
desiredRange=datetime.timedelta(hours=24)
dayRange=now-desiredRange

desiredRange=datetime.timedelta(days=20)
weekRange=now-desiredRange

desiredRange=datetime.timedelta(days=31)
MonthRange=now-desiredRange

FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][0], index_col=0)
FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S') 
toPlot=FullData.loc[str(dayRange) : str(now)] #Select the data based on that
newHour=toPlot.resample('H').sum()  #Resample the data based on hours and sum the data for each hour
print(newHour)

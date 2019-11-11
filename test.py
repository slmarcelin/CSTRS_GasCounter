import pandas as pd
from pandasgui import show
import datetime
import ARD_funct_2 as ard

now=datetime.datetime.now()
desiredRange=datetime.timedelta(hours=24)
dayRange=now-desiredRange

desiredRange=datetime.timedelta(days=20)
weekRange=now-desiredRange

desiredRange=datetime.timedelta(days=31)
MonthRange=now-desiredRange
# ard.folder+"\\"+ard.Files[0][0]
FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][0], index_col=0)
FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S') 
show(FullData)

# img = Image.open(r'image.png')  
# draw = ImageDraw.Draw(img)  
# font = ImageFont.truetype(r'arial.ttf',24)  
# text = 'Welcome to the CSTR GUI\nPlease Select a Gas Counter to view graph rates'
# draw.text((200, 5), text, font = font, align ="center",fill ="black") 
# img=img.save('image.png')
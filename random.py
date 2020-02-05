
def ArdConnect(com):
    global run
    try:
        connection = SerialManager(device=com)  
        ard = ArduinoApi(connection=connection) 
        run = True   
        return ard  
    except:
        run=False  
        return 'EMPTY' 

def ArdSetup(ard):
     global run
     run = True 
     try:
        for i in range(30): 
            ard.pinMode(reed_switch[i], ard.OUTPUT)
            ard.digitalWrite(reed_switch[i], ard.HIGH)
            print('pin # '+str(reed_switch[i])+' is set')
     except:
         run=False
         print('[Arduino setup...Failed]')


def ReadSwitch(ard,PinId):
    global run
    try:
        Pid=int(PinId)
        ticks[Pid-22]=ard.digitalRead(Pid)
    except:
        run=False 
        print("Switch readings Failed!") 


def main(): 
    global mythread
    for x in range(30):
        pinID=x+22;                                          
        mythread = MyThread(name = format(pinID))  
        mythread.start() 
        print("Thread for pin ID #"+str(pinID)+" created\n")
        time.sleep(1)

class MyThread(threading.Thread): 
    def run(self):
        global A 
        while True: 
            if ard.run :  
                value=int(self.getName())     
                connectS="CXN" 
                ard.ReadSwitch(A,value) 
                index=value-22
                current=ard.ticks[index]
                if (current==0): #Debouncing
                    print("Volume increased for Counter of pin ID:"+str(value)) 
                    ard.volume[index]=ard.volume[index]+30 
                    filePath=ard.folder+"\\"+ard.Files[0][index] 
                    fd = open(filePath,'a') 
                    col1=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"," 
                    row=col1+str(ard.volume[index])+"\n"  
                    fd.write(row)
                    fd.flush()
                    fd.close() 
                    time.sleep(2.5) 
                    ard.ticks[index]=1
                time.sleep(0.02) 




def oneDay(): 
    global threading3
    threading3=Timer(WAIT_Day, oneDay)#Set timer for 24 hrs
    threading3.start()
    today=datetime.datetime.now().date() 
    for i in range(30):  
        ard.volume[i]=0 
        filePath=ard.folder+"\\"+ard.Files[0][i] 
        filep=ard.Files[0][i].split(" ")  
        passFile = datetime.datetime.strptime(filep[0], '%Y-%m-%d').date() 
        days=(today-passFile).days
        size=os.path.getsize(filePath)

        if(days>=30 or size>=(10*Mb)): 
            os.remove(filePath)
            ard.Files[0][i]=str(today)+" - GC"+str(i+1)+".csv" 
            filePath=ard.folder+"\\"+ard.Files[0][i]
            fd = open(filePath,'a') 
            firstRow = "Date-Time,Volume\n" 
            fd.write(firstRow) 
            fd.flush()
            fd.close()


def HourRate(index):
    rateType="Hour Rate"
    now=datetime.datetime.now()
    desiredRange=datetime.timedelta(hours=24) #obtain date for last 24 hrs
    dayRange=now-desiredRange 

    FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][index], index_col=0) 
    FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S')
    newHour=toPlot.resample('H').sum()  #Resample the data based on hours
    graphIt(25, newHour, index, rateType,0) 


def WeekRate(index): 
    rateType="Week Rate" 
    now=datetime.datetime.now()
    desiredRange=datetime.timedelta(days=7) #obtain date for last 7 days including today
    WeekRange=now-desiredRange 

    FullData = pd.read_csv(ard.folder+"\\"+ard.Files[0][index], index_col=0) 
    FullData.index= pd.to_datetime(FullData.index,errors='coerce', format='%Y-%m-%d %H:%M:%S')
    toPlot=FullData.loc[str(WeekRange) : str(now)] 
    new_Week=toPlot.resample('D').sum()  #Resample the data based on days
    graphIt(8, new_Week, index, rateType,1) 


    



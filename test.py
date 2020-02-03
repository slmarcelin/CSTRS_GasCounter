

import threading
import time


class MyThread(threading.Thread):
	def run(self):
		print("")
		# while True:
		# 	if ard.run :  #If the arduino is running
		# 		value=self.getName()			
		# 		print("Reading Pin Id {} started!".format(value))        # "Thread-x started!"
		# 		connectS="CXN"
		# 		ard.ReadSwitch(A,value)  #Read the inputs
		# 		index=value-22

		# 		if (not ard.previousTicks[index] and ard.ticks[index])
		# 			ard.volume[index]=ard.volume[index]+30 #Increase the volume for this particular counter
		# 			filePath=ard.folder+"\\"+ard.Files[0][index] #If there is a tick, save to the right csv file
		# 			fd = open(filePath,'a')  #open the csv file that corresponds to the counter
		# 			col1=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"," #The current data
		# 			row=col1+str(ard.volume[index])+"\n"  #The date and the volume of that Gas counter
		# 			fd.write(row) #Write to the file
		# 			fd.flush()
		# 			fd.close()  #close the file
		# 			print(ard.ticks)

		# 		ard.previousTicks[index]=ard.ticks[index]	
		# 		time.sleep(2)                                     
		# 		print("{} finished!".format(self.getName()))       # "Thread-x finished!"

		# 	else:
		# 		print("Port selected:" +com)
		# 		A = ard.ArdConnect(com)
		# 		if ard.run:
		# 			ard.ArdSetup(A)
		# 			connectS="CXN"

def main():
    for x in range(30): 
        pinID=x+22;                                                   # Four times...
        mythread = MyThread(name = format(pinID))  # ...Instantiate a thread and pass a unique ID to it
        mythread.start()                                   # ...Start the thread, invoke the run method
                                            # ...Wait 0.9 seconds before starting another
main()
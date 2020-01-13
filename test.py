import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import threading #for scheduling
style.use('fivethirtyeight')
import os,sys
File='example.txt'
fd = os.open(File,os.O_RDWR)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('example.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)
y=8
def getInput():  #Get input from the Gas counter every 0.25 seconds
    threading.Timer(0.80, getInput).start()  #Set the timer
    y
    y=y-4
    print(y)
    y=y+4
    # row=str(10)+","+str(y)+"\n"  #The date and the volume of that Gas counter
    # os.write(fd,str.encode(row)) #Write to the file




getInput()

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
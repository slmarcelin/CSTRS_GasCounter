import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

fig, ax = plt.subplots()
x, y = 0,0
sc = ax.scatter(x,y)
plt.xlim(0,10)
plt.ylim(0,10)
ann_list = []


def animate(i):
    for i, a in enumerate(ann_list):
        a.remove()

    ann_list[:] = []

    x=float(np.random.rand(1)*10)
    x=round(x,2)
    y=float(np.random.rand(1)*10)
    y=round(y,2)

    ann = plt.annotate((str(x),str(y)),color = "purple", xy=(x, y),size=8)
    ann_list.append(ann)
    sc.set_offsets(np.c_[x,y])

ani = matplotlib.animation.FuncAnimation(fig, animate, 
                frames=2, interval=300, repeat=True) 

plt.show()
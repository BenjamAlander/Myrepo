#matplotlib tutorial
x = [22, 88, 98, 103, 45]
y = [7, 8, 9, 10, 11]
t = [21, 22, 23, 24, 25]

from matplotlib import pyplot as plt
import numpy as np

fig = plt.figure()
axes = fig.add_axes([0.1,0.1,0.8,0.8]) 

axes.plot(t, x, label='x', color="red")
axes.plot(t, y, 'b*', label='y')
axes.set_title("title")
axes.set_ylabel("y")
axes.set_xlabel("t")

fig.savefig('figure1.png')

fig.savefig('figure1.pdf')

fig.show()
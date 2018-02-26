import numpy as np
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from SDAWithVectorField import *
from MovingObstacleSimulator import *
import matplotlib.patches as patches
from datetime import datetime
import sched, time
import threading
import random
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation

fig = plt.figure()
ax = p3.Axes3D(fig)

# create the parametric curve
t=np.arange(0, 2*np.pi, 2*np.pi/100)
x=np.cos(t)
y=np.sin(t)
z=t/(2.*np.pi)

# create the first plot
point, = ax.plot([x[0]], [y[0]], [z[0]], 'o')
line, = ax.plot(x, y, z, label='parametric curve')
ax.legend()
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1.5, 1.5])

# second option - move the point position at every frame
def update_point(n, x, y, z, point):
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z[n], 'z')
    return point

ani=animation.FuncAnimation(fig, update_point, 99, fargs=(x, y, z, point))

plt.show()
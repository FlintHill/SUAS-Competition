from SDAWithVectorField import *
import numpy
import math
from MovingObstacleSimulator import Detector
from MovingObstacleSimulator import Generator
import matplotlib.pyplot as plt
import threading
import time
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import numpy


# plot initial data
generator = Generator()
obstacle_map = generator.generate_obstacle_map()
print(obstacle_map.drone.point)
generator.add_stationary_obstacle(obstacle_map, 6)
waypoint = generator.generate_waypoint()
fig = plt.figure()
ax = p3.Axes3D(fig)
plt.show()


x = numpy.array([obstacle_map.drone.point[0]])
y = numpy.array([obstacle_map.drone.point[1]])
z = numpy.array([0])
print(x)
print(y)

point, = ax.plot([x[0]], [y[0]], [0], 'o')
ax.legend()

def set_value(x, y, z, obstacle_map):
	while obstacle_map.drone.has_reached_waypoint == False:
		obstacle_map.update_repulsive_forces()
		obstacle_map.update_attractive_force()
		avoidance_vector = obstacle_map.get_avoidance_vector()
		unit_velocity = VectorMath.get_single_unit_vector(avoidance_vector)
		new_drone_point = numpy.array([obstacle_map.drone.point[0]+unit_velocity[0], obstacle_map.drone.point[1]+unit_velocity[1],0])
		obstacle_map.set_drone_position(new_drone_point)
		x = numpy.hstack(x, unit_velocity[0])
		y = numpy.hstack(y, unit_velocity[1])
		z = numpy.hstack(z, 0)
	return x,y

x, y =set_value(x, y, z, obstacle_map)

def update_point(n, x, y, z, point):
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z[n], 'z')
    return point

ani=animation.FuncAnimation(fig, update_point, 99, fargs=(x, y, z, point))

plt.show()

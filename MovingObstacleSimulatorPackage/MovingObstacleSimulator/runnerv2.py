from SDAWithVectorField import *
import numpy
import math
from MovingObstacleSimulator import Detector
from MovingObstacleSimulator import Generator
import matplotlib.pyplot as plt
import threading
import time
import mpl_toolkits.mplot3d.axes3d as p3
import numpy
import matplotlib.animation as animation
import multiprocessing


# plot initial data
# generator = Generator()
# obstacle_map = generator.generate_obstacle_map()
# generator.add_stationary_obstacle(obstacle_map, 6)
# waypoint = generator.generate_waypoint()
# obstacle_map.add_waypoint(waypoint)
# fig = plt.figure()
# ax = p3.Axes3D(fig)
# plt.show()

# some scrap

# x = numpy.array([obstacle_map.drone.point[0]])
# y = numpy.array([obstacle_map.drone.point[1]])
# z = numpy.array([0])
# print(x)
# print(y)

# point, = ax.plot([x[0]], [y[0]], [0], 'o')
# ax.legend()

# def set_value(x, y, z, obstacle_map):
# 	while obstacle_map.drone.has_reached_waypoint == False:
# 		obstacle_map.update_repulsive_forces()
# 		obstacle_map.update_attractive_force()
# 		avoidance_vector = obstacle_map.get_avoidance_vector()
# 		unit_velocity = VectorMath.get_single_unit_vector(avoidance_vector)
# 		new_drone_point = numpy.array([obstacle_map.drone.point[0]+unit_velocity[0], obstacle_map.drone.point[1]+unit_velocity[1],0])
# 		obstacle_map.set_drone_position(new_drone_point)
# 		x = numpy.hstack(x, unit_velocity[0])
# 		y = numpy.hstack(y, unit_velocity[1])
# 		z = numpy.hstack(z, 0)
# 	return x,y

# x, y =set_value(x, y, z, obstacle_map)

# def update_point(n, x, y, z, point):
#     point.set_data(np.array([x[n], y[n]]))
#     point.set_3d_properties(z[n], 'z')
#     return point

# ani=animation.FuncAnimation(fig, update_point, 99, fargs=(x, y, z, point))

# plt.show()


#parametric equations for the path(correctness is questionable)

# scrap #2
# x_velocity = obstacle_map.get_avoidance_vector()[0]
# print(x_velocity)
# t_x=numpy.arange(0, obstacle_map.drone.waypoint_holder.get_current_waypoint()[0], VectorMath.get_single_unit_vector(obstacle_map.get_avoidance_vector())[0])
# t_y=numpy.arange(0, obstacle_map.drone.waypoint_holder.get_current_waypoint()[0], VectorMath.get_single_unit_vector(obstacle_map.get_avoidance_vector())[1])
# x=numpy.cos(t)
# y=numpy.sin(t)
# z=0

# point, = ax.plot([x[0]], [y[0]], [z[0]], 'o')
# line, = ax.plot(x, y, z, label='parametric curve')
# ax.legend()
# ax.set_xlim([-2500, 2500])
# ax.set_ylim([-2500, 2500])
# ax.set_zlim([-1.5, 1.5])

# def update_point(n, x, y, z, point):
#     point.set_data(np.array([x[n], y[n]]))
#     point.set_3d_properties(z[n], 'z')
#     return point

# ani=animation.FuncAnimation(fig, update_point, 99, fargs=(x, y, z, point))

# plt.show()

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


my_manager = multiprocessing.Manager()
multi_array = my_manager.list()

generator = Generator()
obstacle_map = generator.generate_obstacle_map()
waypoint = generator.generate_waypoint()
obstacle_map.add_waypoint(waypoint)
generator.add_stationary_obstacle(obstacle_map, 6)
obstacle_map.reset_repulsive_forces()
obstacle_map.reset_attractive_force()
obstacle_map.update_attractive_force()
obstacle_map.update_repulsive_forces()

multi_array.append(obstacle_map)

def makeUpdates(multi_array):
    index = 0
    while True:
        obstacle_map = multi_array[0]
        print(multi_array[0].drone.point)
        obstacle_map.update_repulsive_forces()
        obstacle_map.update_attractive_force()
    	unit_velocity = obstacle_map.get_unit_velocity()
        uav_position = obstacle_map.drone.point
        obstacle_map.set_drone_position(numpy.array([uav_position[0]+unit_velocity[0], uav_position[1]+unit_velocity[1], 0]))
        multi_array[0] = obstacle_map
        index += 1

        time.sleep(0.01)

def animate(i, multi_array):
    ax1.clear()
    ax1.set_xlim([-5000,5000])
    ax1.set_ylim([-5000,5000])
    for obstacle in multi_array[0].obstacles:
        circle_figure = plt.Circle(obstacle.get_point(), obstacle.get_radius(), color="r")
        ax1.add_artist(circle_figure)
        ax1.plot(obstacle.point[0], obstacle.point[1], "bx")
    ax1.plot(multi_array[0].drone.waypoint_holder.get_current_waypoint()[0], multi_array[0].drone.waypoint_holder.get_current_waypoint()[1], "bo")
    ax1.plot(multi_array[0].drone.point[0],multi_array[0].drone.point[0], "go")

multiprocessing.Process(target=makeUpdates, args=(multi_array,)).start()

ani = animation.FuncAnimation(fig, animate, fargs=(multi_array,), interval=1000)
plt.show()
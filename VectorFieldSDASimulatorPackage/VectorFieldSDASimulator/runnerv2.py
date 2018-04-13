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
        # print(multi_array[0].drone.point)
        obstacle_map.reset_repulsive_forces()
        obstacle_map.update_repulsive_forces()
        obstacle_map.update_attractive_force()
        print(obstacle_map.drone.point)
        print(obstacle_map.attractive_force)
        print(obstacle_map.repulsive_forces)
    	unit_velocity = obstacle_map.get_unit_velocity()
        uav_position = obstacle_map.drone.point
        obstacle_map.set_drone_position(numpy.array([uav_position[0]+unit_velocity[0], uav_position[1]+unit_velocity[1], 0]))
        multi_array[0] = obstacle_map
        index += 1

        time.sleep(0.001)

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
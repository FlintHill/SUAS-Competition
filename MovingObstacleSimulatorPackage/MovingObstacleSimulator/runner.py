from SDAWithVectorField import *
import numpy
import math
from MovingObstacleSimulator import Detector
from MovingObstacleSimulator import Generator
import matplotlib.pyplot as plt
import threading
import time




def update_value():
	ax.clear()
	obstacle_map.update_attractive_force()
	obstacle_map.update_repulsive_forces()
	velocity = VectorMath.get_single_unit_vector(obstacle_map.get_avoidance_vector())
	# print(velocity)
	new_drone_point = numpy.array([obstacle_map.drone.point[0] + velocity[0], obstacle_map.drone.point[1] + velocity[1], 0])
	obstacle_map.set_drone_position(new_drone_point)
	if detector.does_collision_happen(obstacle_map):
		print("collision")
	

def plot_graph():
	waypoint = generator.generate_waypoint()
	obstacle_map.add_waypoint(waypoint)
	plt.plot(obstacle_map.drone.point[0], obstacle_map.drone.point[1], "go")
	plt.plot(obstacle_map.drone.waypoint_holder.get_current_waypoint()[0], obstacle_map.drone.waypoint_holder.get_current_waypoint()[1], "bo")
	# print(waypoint)
	for obstacle in obstacle_map.obstacles:
		plt.plot(obstacle.get_point()[0], obstacle.get_point()[1], "bx")
		print("replot_circle")
		circle_figure = plt.Circle(obstacle.get_point(), obstacle.get_radius(), color="r")
		ax.add_artist(circle_figure)
		# print(obstacle.get_point()[0], obstacle.get_point()[1], obstacle.get_radius()) 
	plt.show()

if __name__ == '__main__':
	# generate obstacle map w/ stationary obstacles

	# randomly set the uav's position
	# randomly set a waypoint

	# start
	# while True:
	# 	run avoidance algorithm

	#	update UI

	#	update UAV position
	generator = Generator()
	detector = Detector()
	obstacle_map = generator.generate_obstacle_map()
	generator.add_stationary_obstacle(obstacle_map, 6)
	generator.replace_obstacle_that_covers_the_starting_point(obstacle_map)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	waypoint = generator.generate_waypoint()
	obstacle_map.add_waypoint(waypoint)
	plt.plot(obstacle_map.drone.point[0], obstacle_map.drone.point[1], "go")
	plt.plot(obstacle_map.drone.waypoint_holder.get_current_waypoint()[0], obstacle_map.drone.waypoint_holder.get_current_waypoint()[1], "bo")
	# print(waypoint)
	for obstacle in obstacle_map.obstacles:
			plt.plot(obstacle.get_point()[0], obstacle.get_point()[1], "bx")
			circle_figure = plt.Circle(obstacle.get_point(), obstacle.get_radius(), color="r")
			ax.add_artist(circle_figure)
			# print(obstacle.get_point()[0], obstacle.get_point()[1], obstacle.get_radius()) 
	plt.show()

	while True:
		print("###")
	 	update_value()
	 	plot_graph()
		time.sleep(1)

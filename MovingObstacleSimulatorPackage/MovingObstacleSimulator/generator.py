from SDAWithVectorField import *
from MovingObstacleSimulator import *
import random
import numpy
import math

class Generator(object):

	def __init__(self):
		self.top_right_boundary_point = numpy.array([])
		self.top_left_boundary_point = numpy.array([])
		self.bottom_left_boundary_point = numpy.array([])
		self.bottom_right_boundary_point = numpy.array([])

	def generate_obstacle_map(self):
		"""
		Generate a obstacle map and store its boundary points into the generator
		"""
		flyzone_top_right = numpy.array([random.uniform(1.0, 5000.0), random.uniform(1.0, 5000.0)])
		flyzone_top_left = numpy.array([random.uniform(-5000.0, -1.0), random.uniform(1.0, 5000.0)])
		flyzone_bottom_left = numpy.array([random.uniform(-5000.0, -1.0), random.uniform(-5000.0, -1.0)])
		flyzone_bottom_right = numpy.array([random.uniform(1.0, 5000.0), random.uniform(-5000.0, -1.0)])
		self.top_left_boundary_point = flyzone_top_left
		self.top_right_boundary_point = flyzone_top_right
		self.bottom_left_boundary_point = flyzone_bottom_left
		self.bottom_right_boundary_point = flyzone_bottom_right
		fly_zone = numpy.array([flyzone_top_right, flyzone_top_left, flyzone_bottom_left, flyzone_top_right])
		fly_zones = numpy.array([fly_zone])
		drone_point = numpy.array([0,0,0])
		obstacle_map = ObstacleMap(drone_point, fly_zones)

		return obstacle_map

	def reset_intervalues(self):
		self.top_right_boundary_point = numpy.array([])
		self.top_left_boundary_point = numpy.array([])
		self.bottom_left_boundary_point = numpy.array([])
		self.bottom_right_boundary_point = numpy.array([])

	def generate_stationary_obstacle(self):
		width1 = self.top_right_boundary_point[0] - self.top_left_boundary_point[0]
		width2 = self.bottom_right_boundary_point[0] - self.bottom_left_boundary_point[0]
		length1 = self.top_left_boundary_point[1] - self.bottom_left_boundary_point[1]
		length2 = self.top_right_boundary_point[1] - self.bottom_right_boundary_point[1]
		diagonal_bl_to_tr = math.sqrt((self.top_right_boundary_point[1] - self.bottom_left_boundary_point[1])**2 +(self.top_right_boundary_point[0]- self.bottom_left_boundary_point[0])**2)
		diagonal_br_to_tl = math.sqrt((self.top_left_boundary_point[1] - self.bottom_right_boundary_point[1])**2 +(self.bottom_right_boundary_point[0]- self.top_left_boundary_point[0])**2)
		lines = numpy.array([width1, width2, length1, length2, diagonal_br_to_tl, diagonal_bl_to_tr])
		shortest = 0
		for element in lines:
			if shortest == 0:
				shortest = element
			else:
				if element < shortest:
					shortest = element
		radius = numpy.array([random.uniform(1.0, shortest/4)])
		obstacle_point = numpy.hstack([random.uniform(self.bottom_left_boundary_point[0]+radius, self.top_left_boundary_point[1]-radius), random.uniform(self.bottom_left_boundary_point[0]+radius, self.bottom_right_boundary_point[0]-radius), 0])
		obstacle = StationaryObstacle(obstacle_point, radius, 10)
		return obstacle

	def generate_waypoint(self):
		width1 = self.top_right_boundary_point[0] - self.top_left_boundary_point[0]
		width2 = self.bottom_right_boundary_point[0] - self.bottom_left_boundary_point[0]
		length1 = self.top_left_boundary_point[1] - self.bottom_left_boundary_point[1]
		length2 = self.top_right_boundary_point[1] - self.bottom_right_boundary_point[1]
		diagonal_bl_to_tr = math.sqrt((self.top_right_boundary_point[1] - self.bottom_left_boundary_point[1])**2 +(self.top_right_boundary_point[0]- self.bottom_left_boundary_point[0])**2)
		diagonal_br_to_tl = math.sqrt((self.top_left_boundary_point[1] - self.bottom_right_boundary_point[1])**2 +(self.bottom_right_boundary_point[0]- self.top_left_boundary_point[0])**2)
		lines = numpy.array([width1, width2, length1, length2, diagonal_br_to_tl, diagonal_bl_to_tr])
		shortest = 0
		for element in lines:
			if shortest == 0:
				shortest = element
			else:
				if element < shortest:
					shortest = element
		waypoint = numpy.hstack([random.uniform(self.bottom_left_boundary_point[0], self.top_left_boundary_point[1]), random.uniform(self.bottom_left_boundary_point[0], self.bottom_right_boundary_point[0]), 0])
		return waypoint

	def generate_moving_obstacle_values(self):
		width1 = self.top_right_boundary_point[0] - self.top_left_boundary_point[0]
		width2 = self.bottom_right_boundary_point[0] - self.bottom_left_boundary_point[0]
		length1 = self.top_left_boundary_point[1] - self.bottom_left_boundary_point[1]
		length2 = self.top_right_boundary_point[1] - self.bottom_right_boundary_point[1]
		diagonal_bl_to_tr = math.sqrt((self.top_right_boundary_point[1] - self.bottom_left_boundary_point[1])**2 +(self.top_right_boundary_point[0]- self.bottom_left_boundary_point[0])**2)
		diagonal_br_to_tl = math.sqrt((self.top_left_boundary_point[1] - self.bottom_right_boundary_point[1])**2 +(self.bottom_right_boundary_point[0]- self.top_left_boundary_point[0])**2)
		lines = numpy.array([width1, width2, length1, length2, diagonal_br_to_tl, diagonal_bl_to_tr])
		shortest = 0
		for element in lines:
			if shortest == 0:
				shortest = element
			else:
				if element < shortest:
					shortest = element
		radius = random.uniform(1.0, shortest/2)
		obstacle_point = numpy.array([random.uniform(self.bottom_left_boundary_point[0]+radius, self.top_left_boundary_point[1]-radius), random.uniform(self.bottom_left_boundary_point[0]+radius, self.bottom_right_boundary_point[0]-radius)])
		velocity = random.uniform(1.0, 50.0)
		return obstacle_point, radius, velocity

	def add_stationary_obstacle(self, obstacle_map, quantity):
		loop_index = 0
		while loop_index <= quantity-1:
			stationary_obstacle = self.generate_stationary_obstacle()
			obstacle_map.add_obstacle(stationary_obstacle)
			loop_index += 1

	def add_moving_obstacle(self, obstacle_map, quantity):
		loop_index = 0
		while loop_index <= quantity-1:
			moving_obstacle = MovingObstacleTestingModel(self.generate_moving_obstacle_values())
			obstacle_map.add_obstacle(moving_obstacle)
			loop_index += 1

	def get_boundary_path(self, obstacle_map):
		return obstacle_map.fly_zones.fly_zones.bound_path

	def replace_obstacle_that_covers_the_starting_point(self, obstacle_map):
		"""
		need testing
		"""
		drone_point = numpy.array([0,0,0])
		is_obstacle_obverlapping_with_staring_point = False
		loop_index = 0
		obstacle_to_add = 0
		while loop_index < obstacle_map.obstacles.size:
			distance_from_obstacle = VectorMath.get_magnitude(drone_point, obstacle_map.obstacles[loop_index].point)
			if distance_from_obstacle <= obstacle_map.obstacles[loop_index].radius:
				numpy.delete(obstacle_map.obstacles, loop_index)
				loop_index -= 1
				obstacle_to_add += 1
				is_obstacle_obverlapping_with_staring_point = True

			loop_index += 1
		self.add_stationary_obstacle(obstacle_map, obstacle_to_add)
		if is_obstacle_obverlapping_with_staring_point:
			replace_obstacle_that_covers_the_starting_point(obstacle_map)
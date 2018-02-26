from SDAWithVectorField import *
from .generator import Generator 
import random
import numpy
import math

class Detector(object):

	def __init__(self):
		pass

	def does_collision_happen(self,obstacle_map):
		drone_point = obstacle_map.drone.get_point()
		for obstacle in obstacle_map.obstacles:
			distance_from_obstacle = VectorMath.get_magnitude(drone_point, obstacle.point)
			if distance_from_obstacle <= obstacle.radius:
				return True
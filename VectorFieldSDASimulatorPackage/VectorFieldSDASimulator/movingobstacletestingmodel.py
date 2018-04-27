from SDAWithVectorField import Obstacle
import random
import math

class MovingObstacleTestingModel(object):
	"""docstring for MovingObstacleTestingModel"""
	def __init__(self, starting_point, velocity, radius):
		super(MovingObstacleTestingModel, self).__init__(starting_point)
		self.velocity = velocity
		self.starting_point = starting_point
		self.radius = radius
		self.path = numpy.array([])

	def creat_path(self, generator):
		number_of_waypoints = 5
		while number_of_waypoints > 0:
			waypoint = numpy.array([random.uniform(generator.top_left_boundary_point[0], generator.top_right_boundary_point[0]), random.uniform(generator.bottom_right_boundary_point[1], top_right_boundary_point[1])])
			self.path.append(waypoint)
			number_of_waypoints -= 1

	def reset_path(self):
		self.path = numpy.array([])



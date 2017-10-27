from Obstacle import *
from SDA import Constants

class MovingObstacle(Obstacle)
	

	def __init__(self, point, radius, height, velocity)
		super(MovingObstacle, self).__init__(point, Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS)

		self.radius = radius
		self.height = height
		self.velocity = velocity

	def get_radius(self)

		return self.radius

	def get_height(self)

		return self.height

	def get_velocity(self)

		return self.velocity

	
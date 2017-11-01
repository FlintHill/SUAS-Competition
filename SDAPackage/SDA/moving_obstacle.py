from SDA import Obstacle
from SDA import Constants

class MovingObstacle(Obstacle):
	"""
	sample
	moving_obstacles": [
        {
            "altitude_msl": 189.56748784643966,
            "latitude": 38.141826869853645,
            "longitude": -76.43199876559223,
            "sphere_radius": 150.0
        }
        ]
	"""

    def __init__(self, point, radius):
		"""
		:param point: The point for the stationary obstacle
        :type point: Numpy Array
        :param radius: The radius of the obstacle
        :type radius: Float
        """
		super(MovingObstacle, self).__init__(point, Constants.MOVING_OBSTACLE_SAFETY_RADIUS)

		self.radius = radius

    def get_radius(self):
		"""
        Return the radius of the obstacle plus that of the safety radius
        """
		return self.radius + self.get_safety_radius()
	
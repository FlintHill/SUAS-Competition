import unittest
from SDA import *
import numpy

class MovingObstacleTestCase(unittest.TestCase):
	
	def setUp(self):
		self.point = numpy.array([0,0,0])
		self.radius = 5.0
		
	def test_get_radius(self):
		test_moving_obstacle = MovingObstacle(self.point, self.radius)
		self.assertEqual(test_moving_obstacle.get_safety_radius() + self.radius, test_moving_obstacle.get_radius())



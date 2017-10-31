from SDA import *
import unittest
import numpy

class  MovingObstacleTestCase(object):
	"""docstring for  MovingObstacleTestCase"""
	def setUp(self):
		self.point = numpy.array([0,0,0])
		self.radius = 5
		self.MovingObstacle = MovingObstacle(point, radius)

	def test_get_radius(self):
		self.assrtEqual(35, MovingObstacle.get_radius())



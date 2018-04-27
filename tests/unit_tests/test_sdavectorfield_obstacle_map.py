from SDAWithVectorField import *
import unittest
import numpy

class TestObstacleMap(unittest.TestCase):
	def setUp(self):
		self.test_drone_point = numpy.array([0, 0, 0])
		self.test_fly_zones = numpy.array([numpy.array([(-400, -400),  (-400, 300),  (300, 300),  (300, -400)])])
		self.test_drone_point2 = numpy.array([300, 300, 100])
		self.test_fly_zones2 = numpy.array([numpy.array([(0, 0), (0, 1000), (1000, 1000), (1000, 0)])])
		self.test_drone_point3 = numpy.array([20, 20, 20])
		self.test_drone_point4 = numpy.array([500, 500, 20])
		self.test_drone_point5 = numpy.array([15, 150, 150])
		self.obstacle_map1 = ObstacleMap(self.test_drone_point, self.test_fly_zones)
		self.obstacle_map2 = ObstacleMap(self.test_drone_point2, self.test_fly_zones2)
		self.obstacle_map3 = ObstacleMap(self.test_drone_point3, self.test_fly_zones2)
		self.obstacle1 = MovingObstacle(numpy.array([50,50,50]), 10)
		self.obstacle2 = MovingObstacle(numpy.array([200,200,200]), 10)
		self.waypoint = numpy.array([100,100,100])
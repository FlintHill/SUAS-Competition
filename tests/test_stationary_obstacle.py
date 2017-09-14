import unittest
from SDA import *
import numpy

class TestSDAStationaryObstacle(unittest.TestCase):

    def setUp(self):
        self.point = numpy.array([0,0,0])
        self.radius = 1.0
        self.height = 1.0

    def test_get_radius(self):
        test_stationary_obstacle = StationaryObstacle(self.point, self.radius, self.height)
        self.assertEqual(test_stationary_obstacle.get_radius(), test_stationary_obstacle.get_safety_radius() + self.radius)

    def test_get_height(self):
        test_stationary_obstacle = StationaryObstacle(self.point, self.radius, self.height)
        self.assertEqual(test_stationary_obstacle.get_height(), self.height)

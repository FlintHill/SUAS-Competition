import unittest
from SDA import *
import numpy

class TestSDAObstacle(unittest.TestCase):

    def setUp(self):
        self.point = numpy.array([25,25,25])
        self.safety_radius = 45

    def test_get_safety_radius(self):
        test_obstacle = Obstacle(self.point, self.safety_radius)
        self.assertEqual(test_obstacle.get_safety_radius(), self.safety_radius)

    def test_get_point(self):
        test_obstacle = Obstacle(self.point, self.safety_radius)
        self.assertEqual(test_obstacle.get_point()[2], self.point[2])

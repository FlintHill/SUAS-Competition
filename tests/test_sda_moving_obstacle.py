import unittest
from SDA import *
import numpy

class TestSDAMovingObstacle(unittest.TestCase):

    def setUp(self):
        self.point = numpy.array([0,0,0])
        self.radius = 1.0
        self.speed = 1.0

    def test_get_radius(self):
        test_moving_obstacle = MovingObstacle(self.point, self.radius, self.speed)
        self.assertEqual(test_moving_obstacle.get_radius(), ((test_moving_obstacle.get_safety_radius() + self.radius) * self.speed / 10.0))

    def test_get_speed(self):
        test_moving_obstacle = MovingObstacle(self.point, self.radius, self.speed)
        self.assertEqual(test_moving_obstacle.get_speed(), self.speed)

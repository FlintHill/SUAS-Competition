from abc import abstractmethod
from abc import ABCMeta
from SDA import*
import numpy as np
import unittest

class ObstacleTestCase(unittest.TestCase):

    def setUp(self):

        my_point = np.array([2, 3, 3])
        my_safety_radius = 2.33
        self.my_obstacle = Obstacle(my_point, my_safety_radius)

    def test_get_safety_radius(self):

        self.assertEqual(self.my_obstacle.get_safety_radius(), 2.33)

    def test_get_point(self):

        self.assertTrue(np.array_equal(self.my_obstacle.get_point(), np.array([2, 3, 3])))

from SDA import *
import numpy as np
from SUASSystem import *
import unittest

class FlightBoundaryContainerTestCase(unittest.TestCase):

    def setUp(self):
        self.boundary = FlightBoundariesContainer(np.array([np.array([[-2000, -2000], [-2000, 2000], [2000, 2000], [2000, -2000]])]))

    def test_is_point_in_bounds(self):
        self.assertTrue(self.boundary.is_point_in_bounds(np.array([0,0,0])))

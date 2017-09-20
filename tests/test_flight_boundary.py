from matplotlib.path import Path
from SDA import*
import unittest
import numpy as np

class FlightBoundaryTestCase(unittest.TestCase):

    def setUp(self):

        my_min_altitude = 50
        my_max_altitude = 200
        my_bound_path = Path(np.array([[100,100],[100,100]]))
        self.my_flight_boundary = FlightBoundary(my_min_altitude, my_max_altitude, my_bound_path)

    def test_is_point_in_bounds(self):

        my_point = np.array([50, 50, 100])
        self.assertTrue(my_flight_boundary.is_point_in_bounds(my_point), True)

    def test_path_method(self):

        my_point = np.array([50, 50, 100])
        self.assertTrue(path_method(my_point), True)

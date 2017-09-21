from matplotlib.path import Path
from SDA import*
import unittest
import numpy as np

class FlightBoundaryTestCase(unittest.TestCase):

    def setUp(self):

        my_min_altitude = 50.0
        my_max_altitude = 200.0
        my_boundary_waypoints = np.array([(0,0),(0,100),(100,100),(100,0)])
        my_bound_path = Path(my_boundary_waypoints)
        self.my_flight_boundary = FlightBoundary(my_min_altitude, my_max_altitude, my_boundary_waypoints)

    def test_is_point_in_bounds(self):

        my_point = np.array([50, 50, 100])
        print self.my_flight_boundary.is_point_in_bounds(my_point)
        self.assertTrue(self.my_flight_boundary.is_point_in_bounds(my_point), True)

    def test_path_method(self):

        my_point = np.array([50, 50])
        self.assertTrue(self.my_flight_boundary.path_method(my_point), True)

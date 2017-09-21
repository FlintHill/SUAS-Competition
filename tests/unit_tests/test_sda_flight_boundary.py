from matplotlib.path import Path
from SDA import*
import unittest
import numpy as np

class FlightBoundaryTestCase(unittest.TestCase):

    def setUp(self):

        my_min_altitude = 50.0
        my_max_altitude = 200.0
        my_bound_path = np.array([(0,0),(0,100),(100,100),(100,0)])
        self.my_flight_boundary = FlightBoundary(my_min_altitude, my_max_altitude, my_bound_path)

    def test_is_point_in_bounds(self):

        my_point = np.array([50, 50, 100])
        print self.my_flight_boundary.is_point_in_bounds(my_point)
        self.assertTrue(self.my_flight_boundary.is_point_in_bounds(my_point), True)

    def is_point_in_bounds(self, point):
        """
        Returns True if the passed point is in the boundaries, False if not

        :param point: The point to test
        :type point: Numpy Array
        """
        dim_reduced_point = point[:2]
        is_point_in_polygon = self.path_method(dim_reduced_point)
        is_point_in_alts = (point[2] > self.min_altitude and point[2] < self.max_altitude)

        if is_point_in_polygon and is_point_in_alts:
            return True

        return False


    def test_path_method(self):
        my_bound_path = Path([(0,0),(0,100),(100,100),(100,0)])
        my_point = np.array([[50, 50]])
        self.assertTrue(my_bound_path.contains_points([my_point]), True)

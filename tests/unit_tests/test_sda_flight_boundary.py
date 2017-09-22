from matplotlib.path import Path
from SDA import *
import unittest
import numpy

class FlightBoundaryTestCase(unittest.TestCase):

    def setUp(self):

        test_min_altitude = 50.0
        test_max_altitude = 200.0
        test_boundary_waypoints = numpy.array([(0,0),(0,100),(100,100),(100,0)])
        test_bound_path = Path(test_boundary_waypoints)
        self.test_flight_boundary = FlightBoundary(test_min_altitude, test_max_altitude, test_boundary_waypoints)

    def test_is_point_in_bounds(self):

        test_point = numpy.array([50, 50, 100])
        print self.test_flight_boundary.is_point_in_bounds(test_point)
        self.assertTrue(self.test_flight_boundary.is_point_in_bounds(test_point), True)

    def test_path_method(self):

        test_point = numpy.array([50, 50])
        self.assertTrue(self.test_flight_boundary.path_method(test_point), True)

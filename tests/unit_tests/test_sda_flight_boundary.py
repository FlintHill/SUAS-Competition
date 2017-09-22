from matplotlib.path import Path
from SDA import *
import unittest
import numpy

class FlightBoundaryTestCase(unittest.TestCase):

    def setUp(self):

        test_min_altitude1 = 50.0
        test_max_altitude1 = 200.0

        test_min_altitude2 = -300.0
        test_max_altitude2 = -50.0

        test_boundary_waypoints1 = numpy.array([(0,0),(0,100),(100,100),(100,0)])
        test_boundary_waypoints2 = numpy.array([(-25,0),(50,50),(0,100),(-100,150),(100,150),(150,0),(50,-50),(0,-100),(100,-150),(-100,-150)])

        test_bound_path1 = Path(test_boundary_waypoints1)
        test_bound_path2 = Path(test_boundary_waypoints2)

        self.test_flight_boundary1 = FlightBoundary(test_min_altitude1, test_max_altitude1, test_boundary_waypoints1)
        self.test_flight_boundary2 = FlightBoundary(test_min_altitude2, test_max_altitude2, test_boundary_waypoints2)

    def test_is_point_in_bounds(self):

        test_point1 = numpy.array([50, 50, 100])
        test_point2 = numpy.array([1, 1, 51])
        test_point3 = numpy.array([99, 99, 199])
        test_point4 = numpy.array([1, 1, 50])
        test_point5 = numpy.array([99, 99, 200])
        test_point6 = numpy.array([50, 50, 49])
        test_point7 = numpy.array([50, 50, 201])

        self.assertTrue(self.test_flight_boundary1.is_point_in_bounds(test_point1))
        self.assertTrue(self.test_flight_boundary1.is_point_in_bounds(test_point2))
        self.assertTrue(self.test_flight_boundary1.is_point_in_bounds(test_point3))
        self.assertFalse(self.test_flight_boundary1.is_point_in_bounds(test_point4))
        self.assertFalse(self.test_flight_boundary1.is_point_in_bounds(test_point5))
        self.assertFalse(self.test_flight_boundary1.is_point_in_bounds(test_point6))
        self.assertFalse(self.test_flight_boundary1.is_point_in_bounds(test_point7))

        test_point8 = numpy.array([100, 100, -150])
        test_point9 = numpy.array([50, 51, -299])
        test_point10 = numpy.array([0, 101, -51])
        test_point11 = numpy.array([-49, 0, -300])
        test_point12 = numpy.array([-50, -100, -50])
        test_point13 = numpy.array([100, 149, -301])
        test_point14 = numpy.array([-99, 149, -49])

        self.assertTrue(self.test_flight_boundary2.is_point_in_bounds(test_point8))
        self.assertTrue(self.test_flight_boundary2.is_point_in_bounds(test_point9))
        self.assertTrue(self.test_flight_boundary2.is_point_in_bounds(test_point10))
        self.assertFalse(self.test_flight_boundary2.is_point_in_bounds(test_point11))
        self.assertFalse(self.test_flight_boundary2.is_point_in_bounds(test_point12))
        self.assertFalse(self.test_flight_boundary2.is_point_in_bounds(test_point13))
        self.assertFalse(self.test_flight_boundary2.is_point_in_bounds(test_point14))

    def test_path_method(self):

        test_point1 = numpy.array([50, 50])
        test_point2 = numpy.array([1, 1])
        test_point3 = numpy.array([99, 99])
        test_point4 = numpy.array([0, 0])
        test_point5 = numpy.array([100, 100])
        test_point6 = numpy.array([101, 99])
        test_point7 = numpy.array([1, -1])

        self.assertTrue(self.test_flight_boundary1.path_method(test_point1))
        self.assertTrue(self.test_flight_boundary1.path_method(test_point2))
        self.assertTrue(self.test_flight_boundary1.path_method(test_point3))
        self.assertFalse(self.test_flight_boundary1.path_method(test_point4))
        self.assertFalse(self.test_flight_boundary1.path_method(test_point5))
        self.assertFalse(self.test_flight_boundary1.path_method(test_point6))
        self.assertFalse(self.test_flight_boundary1.path_method(test_point7))

        test_point8 = numpy.array([49, 49])
        test_point9 = numpy.array([0, 101])
        test_point10 = numpy.array([99, -149.8])
        test_point11 = numpy.array([-99, 149])
        test_point12 = numpy.array([40, 50])
        test_point13 = numpy.array([0, -150])
        test_point14 = numpy.array([40, -100])

        self.assertTrue(self.test_flight_boundary2.path_method(test_point8))
        self.assertTrue(self.test_flight_boundary2.path_method(test_point9))
        self.assertTrue(self.test_flight_boundary2.path_method(test_point10))
        self.assertFalse(self.test_flight_boundary2.path_method(test_point11))
        self.assertFalse(self.test_flight_boundary2.path_method(test_point12))
        self.assertFalse(self.test_flight_boundary2.path_method(test_point13))
        self.assertFalse(self.test_flight_boundary2.path_method(test_point14))

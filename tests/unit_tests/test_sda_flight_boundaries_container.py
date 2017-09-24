from SDA import *
import unittest
import numpy

class FlightBoundariesContainerTestCase(unittest.TestCase):

    def setUp(self):
        fly_zones = numpy.array([numpy.array([(0,0),(0,100),(100,100),(100,0)]),numpy.array([(-200,0),(-200,-200),(0,-200),(0,0)])])
        test_fly_zones = numpy.array([FlightBoundary(Constants.MIN_ALT, Constants.MAX_ALT, boundary_points) for boundary_points in fly_zones])
        self.test_flight_boundaries_container = FlightBoundariesContainer(fly_zones)

    def test_is_point_in_bounds(self):
        test_point1 = numpy.array([20, 30, 40])
        self.assertTrue(self.test_flight_boundaries_container.is_point_in_bounds(test_point1))
        test_point2 = numpy.array([1000, 1000, 1000])
        self.assertFalse(self.test_flight_boundaries_container.is_point_in_bounds(test_point2))

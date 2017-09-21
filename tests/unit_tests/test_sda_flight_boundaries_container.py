from SDA import *
import unittest
import numpy as np

class FlightBoundariesContainerTestCase(unittest.TestCase):

    def setUp(self):

        fly_zones = np.array([np.array([(0,0),(0,100),(100,100),(100,0)]),np.array([(-200,0),(-200,-200),(0,-200),(0,0)])])
        my_fly_zones = np.array([FlightBoundary(Constants.MIN_ALT, Constants.MAX_ALT, boundary_points) for boundary_points in fly_zones])
        self.my_flight_boundaries_container = FlightBoundariesContainer(fly_zones)

    def test_is_point_in_bounds(self):

        my_point1 = np.array([20, 30, 40])
        self.assertTrue(self.my_flight_boundaries_container.is_point_in_bounds(my_point1), True)
        my_point2 = np.array([1000, 1000, 1000])
        self.assertFalse(self.my_flight_boundaries_container.is_point_in_bounds(my_point2), True)

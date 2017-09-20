from SDA import *
import unittest
import numpy as np

class FlightBoundariesContainerTestCase(unittest.TestCase):

    def setUp(self):

        my_fly_zones = np.array([FlightBoundary(Constants.MIN_ALT, Constants.MAX_ALT, boundary_points) for boundary_points in fly_zones])
        self.my_flight_boundaries_container = FlightBoundariesContainer(my_fly_zones)

    def test_is_point_in_bounds(self):

        my_point = np.array([20, 30])

        self.assertTrue(FlightBoundariesContainer.is_point_in_bounds(my_point))

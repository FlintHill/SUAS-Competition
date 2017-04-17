from math_functions import *
import math
import numpy
from location_data import Location
import unittest

class MathFunctionsTestCase(unittest.TestCase):

    def test_haversine(self):
        """
        Test the haversine math
        """
        location1 = Location(38.8703041, -77.3214035, 100)
        location2 = Location(38.8739395, -77.3245697, 100)
        actual_dist = 488.40475398671807

        haversine_dist = haversine(location1, location2)

        self.assertTrue(abs(actual_dist - haversine_dist) < 0.1)

    def test_inverse_haversine(self):
        """
        Test the inverse haversine math
        """
        location1 = Location(38.8703041, -77.3214035, 100)
        actual_location2 = Location(38.8739395, -77.3245697, 100)
        dist = haversine(location1, actual_location2)
        diff_bearing = bearing(location1, actual_location2)
        diff = [math.cos(diff_bearing) * dist, math.sin(diff_bearing) * dist, 100]

        inverse_haversine_gps = inverse_haversine(location1, diff, diff_bearing)

        self.assertTrue(abs(inverse_haversine_gps.get_lat() - actual_location2.get_lat()) < 0.001)
        self.assertTrue(abs(inverse_haversine_gps.get_lon() - actual_location2.get_lon()) < 0.001)

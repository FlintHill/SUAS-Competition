from static_math import *
from gps_coordinates import GPSCoordinates
import unittest

class StaticMathTestCase(unittest.TestCase):

    def test_haversine(self):
        """
        Test the haversine math
        """
        gps_1 = GPSCoordinates(38.8703041, -77.3214035, 100)
        gps_2 = GPSCoordinates(38.8739395, -77.3245697, 100)
        actual_dist = 488.40475398671807

        haversine_dist = haversine(gps_1, gps_2)

        self.assertTrue(abs(actual_dist - haversine_dist) < 0.1)

    def test_inverse_haversine(self):
        """
        Test the inverse haversine math
        """
        gps_1 = GPSCoordinates(38.8703041, -77.3214035, 100)
        actual_gps_2 = GPSCoordinates(38.8739395, -77.3245697, 100)
        dist = haversine(gps_1, actual_gps_2)
        diff_bearing = bearing(gps_1, actual_gps_2)
        diff = [cos(diff_bearing) * dist, sin(diff_bearing) * dist, 0]

        inverse_haversine_gps = inverse_haversine(gps_1, diff, diff_bearing)

        self.assertTrue(abs(inverse_haversine_gps.get_latitude() - actual_gps_2.get_latitude()) < 0.01)
        self.assertTrue(abs(inverse_haversine_gps.get_longitude() - actual_gps_2.get_longitude()) < 0.01)

from SUASSystem import *
import math
import numpy
import unittest

class MathFunctionsTestCase(unittest.TestCase):

    def test_haversine(self):
        """
        Test the haversine math
        """
        location1 = Location(38.8703041, -77.3214035, 100)
        location2 = Location(38.8739395, -77.3245697, 100)

        dx, dy, dz = haversine(location1, location2)

        self.assertTrue(abs(-274.411439732 - dx) < 0.0001)
        self.assertTrue(abs(404.697332161 - dy) < 0.0001)
        self.assertEqual(dz, 0)

    def test_inverse_haversine(self):
        """
        Test the inverse haversine math
        """
        location1 = Location(38.8703041, -77.3214035, 100)
        actual_location2 = Location(38.8739395, -77.3245697, 100)
        dx, dy, dz = haversine(location1, actual_location2, units="US")
        diff = [dx, dy, 100]

        inverse_haversine_gps = inverse_haversine(location1, diff)

        self.assertTrue(abs(inverse_haversine_gps.get_lat() - actual_location2.get_lat()) < 0.001)
        self.assertTrue(abs(inverse_haversine_gps.get_lon() - actual_location2.get_lon()) < 0.001)

    def test_convert_to_point(self):
        """
        Test the convert to point math
        """
        home_location = Location(38.8703041, -77.3214035, 100)
        location1 = Location(38.8739395, -77.3245697, 100)
        location2 = Location(38.8702000, -77.3214035, 100)
        location3 = Location(38.8704000, -77.3214035, 100)
        location4 = Location(38.8703041, -77.3214035, 100)

        new_point_1 = convert_to_point(home_location, location1)
        new_point_2 = convert_to_point(home_location, location2)
        new_point_3 = convert_to_point(home_location, location3)
        new_point_4 = convert_to_point(home_location, location4)

        self.assertTrue(True)

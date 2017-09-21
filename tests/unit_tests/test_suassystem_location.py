import unittest
import numpy
import dronekit
from SUASSystem import *
from dronekit import LocationGlobalRelative

class LocationTestCase(unittest.TestCase):

    def setUp(self):

        lat_one = 100
        lon_one = 120
        alt_one = 140

        self.my_location = Location(lat_one, lon_one, alt_one)

    def test_get_lat(self):

        self.assertEqual(self.my_location.get_lat(), 100)

    def test_get_lon(self):

        self.assertEqual(self.my_location.get_lon(), 120)

    def test_get_alt(self):

        self.assertEqual(self.my_location.get_alt(), 140)

    def test_repr(self):
       self.assertEquals('Lat: 100 Lon: 120 Alt: 140', self.my_location.__repr__())

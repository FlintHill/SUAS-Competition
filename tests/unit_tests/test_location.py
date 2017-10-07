from SUASSystem import *
import math
import numpy
import unittest
from dronekit import LocationGlobalRelative

class locationTestCase(unittest.TestCase):

    def setUp(self):
        self.position = Location(5, 12, 20)

    def test_get_lat(self):
        self.assertEquals(5, self.position.get_lat())

    def test_get_lon(self):
        self.assertEquals(12, self.position.get_lon())

    def test_get_alt(self):
        self.assertEquals(20, self.position.get_alt())

    def test__repr__(self):
        self.assertEquals('Lat: 5 Lon: 12 Alt: 20', self.position.__repr__())

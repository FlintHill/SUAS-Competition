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

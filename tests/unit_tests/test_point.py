import numpy
from SyntheticDataset import *
import unittest
import math

class PointTestCase(unittest.TestCase):

    def setUp(self):
        self.x_init = 2
        self.y_init = 3
        self.point = Point(self.x_init, self.y_init)

    def test_get_x(self):
        self.assertEquals(self.x_init, self.point.getX())

    def test_get_y(self):
        self.assertEquals(self.y_init, self.point.getY())

    def test_set_x(self):
        self.point.x = 5
        self.assertEquals(5, self.point.getX())

    def test_set_y(self):
        self.point.y = 5
        self.assertEquals(5, self.point.getY())

    def test___getitem__(self):
        self.assertEquals(3, self.point.__getitem__(1))

    def test_get_translate_point(self):
        self.point1 = self.point.getTranslatePoint(Point(3,4))
        self.assertEquals((1,1), (self.point1.getX(), self.point1.getY()))

    def test_get_translated_point(self):
        self.point2 = self.point.getTranslatedPoint(Point(1,1))
        self.assertEquals((3,4), (self.point2.getX(), self.point2.getY()))

    def test_to_int(self):
        self.point3 = self.point.toInt()
        self.assertEquals((2,3), (self.point3.toInt().getX(), self.point3.toInt().getY()))

    def test_rotate(self):
        pivot = Point(0,0)
        spin = math.pi
        self.point.rotate(pivot, spin)
        #rounded to 6 digits as the method returns a 1 in the 8th decimal position. 6 decimals is easily enough for acccuracy
        self.assertEquals((-2.000000,-3.000000), (round(self.point.getX(), 6), round(self.point.getY(), 6)))

import numpy as np
from SyntheticDataset import *
import unittest
import math

class PointTestCase(unittest.TestCase):

    def setUp(self):
        self.xInit = 2
        self.yInit = 3
        self.point = Point(self.xInit, self.yInit)

    def test_get_X(self):
        self.assertEquals(self.xInit, self.point.getX())

    def test_get_Y(self):
        self.assertEquals(self.yInit, self.point.getY())

    def test_set_X(self):
        self.point.x = 5
        self.assertEquals(5, self.point.getX())

    def test_set_Y(self):
        self.point.y = 5
        self.assertEquals(5, self.point.getY())

    def test___getitem__(self):
        self.assertEquals(3, self.point.__getitem__(1))

    def test_getTranslatePoint(self):
        self.point1 = self.point.getTranslatePoint(Point(3,4))
        self.assertEquals((1,1), (self.point1.getX(), self.point1.getY()))

    def test_getTranslatedPoint(self):
        self.point2 = self.point.getTranslatedPoint(Point(1,1))
        self.assertEquals((3,4), (self.point2.getX(), self.point2.getY()))

    def test_toInt(self):
        self.point3 = self.point.toInt()
        self.assertEquals((2,3), (self.point3.toInt().getX(), self.point3.toInt().getY()))

    def test_rotate(self):
        pivot = Point(0,0)
        spin = math.pi
        self.point.rotate(pivot, spin)
        self.assertEquals((-2.000000,-3.000000), (round(self.point.getX(), 6), round(self.point.getY(), 6)))

import numpy as np
from SyntheticDataset import *
import unittest

class RectangleTestCase(unittest.TestCase):

    def setUp(self):
        self.height = 8
        self.x_initial = 0
        self.y_initial = 0
        self.width = 6
        self.rectangle = Rectangle(self.x_initial, self.y_initial, self.width, self.height)

    def test__repr__(self):
        self.assertEquals("X: 0 Y: 0 Width: 6 Height: 8", self.rectangle.__repr__())

    def test_get_Height(self):
        self.assertEquals(8, self.rectangle.getHeight())

    def test_get_Width(self):
        self.assertEquals(6, self.rectangle.getWidth())

    def test_get_X(self):
        self.assertEquals(0, self.rectangle.getX())

    def test_get_Y(self):
        self.assertEquals(0, self.rectangle.getY())

    def test_set_X(self):
        self.rectangle.setX(5)
        self.assertEquals(5, self.rectangle.getX())

    def test_set_Y(self):
        self.rectangle.setY(5)
        self.assertEquals(5, self.rectangle.getY())

    def test_set_Width(self):
        self.rectangle.setWidth(100)
        self.assertEquals(100, self.rectangle.getWidth())

    def test_set_Height(self):
        self.rectangle.setHeight(100)
        self.assertEquals(100, self.rectangle.getHeight())

    def test_contains(self):
        self.assertTrue(self.rectangle.contains(Point(1,1)))

    def test_get_Mid_point(self):
        self.assertEquals((3,4), (self.rectangle.getX() + (self.rectangle.getWidth()/2), self.rectangle.getY() + (self.rectangle.getHeight()/2)))

    def test_intersects(self):
        self.assertTrue(Rectangle(1, 1, 2, 2))

    def test_fill(self):
        pass
        #TODO: contact peter and revisit (img vs image)
        #self.rectangle.fill(   ,    ,(20,20,20,255))

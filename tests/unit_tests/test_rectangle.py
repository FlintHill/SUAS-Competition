import numpy
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

    def test_get_height(self):
        self.assertEquals(8, self.rectangle.getHeight())

    def test_get_width(self):
        self.assertEquals(6, self.rectangle.getWidth())

    def test_get_x(self):
        self.assertEquals(0, self.rectangle.getX())

    def test_get_y(self):
        self.assertEquals(0, self.rectangle.getY())

    def test_set_x(self):
        self.rectangle.setX(5)
        self.assertEquals(5, self.rectangle.getX())

    def test_set_y(self):
        self.rectangle.setY(5)
        self.assertEquals(5, self.rectangle.getY())

    def test_set_width(self):
        self.rectangle.setWidth(100)
        self.assertEquals(100, self.rectangle.getWidth())

    def test_set_height(self):
        self.rectangle.setHeight(100)
        self.assertEquals(100, self.rectangle.getHeight())

    def test_contains(self):
        self.rectangle.setWidth(100)
        self.rectangle.setHeight(100)
        self.assertTrue(self.rectangle.contains(Point(1,1)))
        self.assertTrue(self.rectangle.contains(Point(20,10)))
        self.assertFalse(self.rectangle.contains(Point(200,10)))
        self.assertFalse(self.rectangle.contains(Point(-1,0)))

    def test_get_mid_point(self):
        self.assertEquals((3,4), (self.rectangle.getX() + (self.rectangle.getWidth()/2), self.rectangle.getY() + (self.rectangle.getHeight()/2)))

    def test_intersects(self):
        self.intersecting_rectangle = Rectangle(1, 1, 2, 2)
        self.assertTrue(self.rectangle.intersects(self.intersecting_rectangle))

    def test_fill(self):
        pass
        #TODO: contact peter and revisit (img vs image)
        #self.rectangle.fill(   ,    ,(20,20,20,255))

from SyntheticDataset.image_operations import Line
from SyntheticDataset.image_operations import Point
import unittest
from math import sqrt

class LineTestCase(unittest.TestCase):

    def test_set_slope(self):
        L = Line(Point(1,2),Point(5,10))
        L.setSlope()
        self.assertEqual(2, L.slope)

    def test_get_Y_as_function(self):
        L= Line(Point(1,2),Point(5,10))
        y_value = L.getYAsFunction(1)
        self.assertEqual(2, y_value)

    def test_get_X_parametric(self):
        L = Line(Point(1,2),Point(5,10))
        x_parametric = L.getXParametric(2)
        self.assertEqual(9, x_parametric)

    def test_get_Y_parametric(self):
        L = Line(Point(1,2),Point(5,10))
        y_parametric = L.getYParametric(2)
        self.assertEqual(18, y_parametric)

    def test_get_DX(self):
        L = Line(Point(1,2),Point(5,10))
        dx = L.getDX()
        self.assertEqual(4, dx)

    def test_get_DY(self):
        L = Line(Point(1,2),Point(5,10))
        dy = L.getDY()
        self.assertEqual(8, dy)

    def test_get_magnitude(self):
        L = Line(Point(1,2),Point(5,10))
        magnitude = L.getMagnitude()
        self.assertEqual(sqrt(80), magnitude)

        """
        This next one isnt done
        """
    def test_get_slope(self):
        L = Line(Point(1,2),Point(5,10))
        slope1 = L.getSlope()
        self.assertEqual(2, slope1)

    def test_get_p1(self):
        L = Line(Point(1,2),Point(5,10))
        self.P1 = L.getP1()
        self.assertEqual(Point(1,2).getX(), self.P1.getX())
        self.assertEqual(Point(1,2).getY(), self.P1.getY())

    def test_get_p2(self):
        L = Line(Point(1,2),Point(5,10))
        self.P2 = L.getP2()
        self.assertEqual(Point(5,10).getX(), self.P2.getX())
        self.assertEqual(Point(5,10).getY(), self.P2.getY())

    def test_get_b(self):
        L = Line(Point(1,2),Point(5,10))
        B = L.getB()
        self.assertEqual(4, B)

from SyntheticDataset.image_operations import Line
from SyntheticDataset.image_operations import Point
import unittest
from math import sqrt

class LineTestCase(unittest.TestCase):

    def test_set_slope(self):
        test_line = Line(Point(1,2),Point(5,10))
        test_line.setSlope()
        self.assertEqual(2, test_line.slope)

    def test_get_Y_as_function(self):
        test_line = Line(Point(1,2),Point(5,10))
        y_value = test_line.getYAsFunction(1)
        self.assertEqual(2, y_value)

    def test_get_X_parametric(self):
        test_line = Line(Point(1,2),Point(5,10))
        x_parametric = test_line.getXParametric(2)
        self.assertEqual(9, x_parametric)

    def test_get_Y_parametric(self):
        test_line = Line(Point(1,2),Point(5,10))
        y_parametric = test_line.getYParametric(2)
        self.assertEqual(18, y_parametric)

    def test_get_DX(self):
        test_line = Line(Point(1,2),Point(5,10))
        dx = test_line.getDX()
        self.assertEqual(4, dx)

    def test_get_DY(self):
        test_line = Line(Point(1,2),Point(5,10))
        dy = test_line.getDY()
        self.assertEqual(8, dy)

    def test_get_magnitude(self):
        test_line = Line(Point(1,2),Point(5,10))
        magnitude = test_line.getMagnitude()
        self.assertEqual(sqrt(80), magnitude)

    def test_get_slope(self):
        test_line = Line(Point(1,2),Point(5,10))
        slope1 = test_line.getSlope()
        self.assertEqual(2, slope1)

    def test_get_p1(self):
        test_line = Line(Point(1,2),Point(5,10))
        self.P1 = test_line.getP1()
        self.assertEqual(Point(1,2).getX(), self.P1.getX())
        self.assertEqual(Point(1,2).getY(), self.P1.getY())

    def test_get_p2(self):
        test_line = Line(Point(1,2),Point(5,10))
        self.P2 = test_line.getP2()
        self.assertEqual(Point(5,10).getX(), self.P2.getX())
        self.assertEqual(Point(5,10).getY(), self.P2.getY())

    def test_get_b(self):
        test_line = Line(Point(1,2),Point(5,10))
        B = test_line.getB()
        self.assertEqual(4, B)

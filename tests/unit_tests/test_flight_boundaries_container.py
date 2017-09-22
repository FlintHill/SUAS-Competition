from SDA import *
import numpy
from SUASSystem import *
import unittest

class FlightBoundaryContainerTestCase(unittest.TestCase):

    def setUp(self):
        self.test_boundary_container = FlightBoundariesContainer(numpy.array([[[-2000, -2000], [-2000, 2000], [2000, 2000], [2000, -2000]], [[-5000, -1000], [-4500, 2000], [2000, 2000], [2000, -2000]]]))
        self.test_boundary_container1 = FlightBoundariesContainer(numpy.array([numpy.array([[-2000, -2000], [-1500, 2000], [2000, 4500], [1500, -3000]])]))
        self.test_boundary_container2 = FlightBoundariesContainer(numpy.array([numpy.array([[-2000, -2000], [-2000, 2000], [0,1000], [2000, 2000], [2000, -2000]])]))
    def test_is_point_in_bounds(self):
        self.assertTrue(self.test_boundary_container.is_point_in_bounds(numpy.array([0,0,0])))
        self.assertTrue(self.test_boundary_container.is_point_in_bounds(numpy.array([10,0,1])))
        self.assertTrue(self.test_boundary_container1.is_point_in_bounds(numpy.array([0,0,0])))
        self.assertTrue(self.test_boundary_container1.is_point_in_bounds(numpy.array([100, 100,100])))
        self.assertFalse(self.test_boundary_container2.is_point_in_bounds(numpy.array([-8000,0,0])))

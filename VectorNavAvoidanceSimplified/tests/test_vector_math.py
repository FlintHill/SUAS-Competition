import unittest
from ObjAvoidSimplified import *

class VectorMathTestCase(unittest.TestCase):

    def test_distance(self):
        """
        Test the algorithm to determine the distance between two points
        """
        point_one = np.array([0, 0])
        point_two = np.array([10, 10])

        dist = VectorMath.get_magnitude(point_one, point_two)

        self.assertEqual(dist, 200**0.5)

    def test_force(self):
        """
        Test the algorithm to determine the gravitational forces of two
        masses
        """
        mass_one = Mass([0, 0], 10)
        mass_two = Mass([10, 10], 10)
        scale = 5000

        force = VectorMath.get_force(mass_one, mass_two, scale)

        self.assertEqual(int(force + 0.5), 2500)

    def test_unit_vector(self):
        """
        Test the algorithm to determine two points' unit vector
        """
        point_one = np.array([0, 0])
        point_two = np.array([10, 10])

        unit_vector = VectorMath.get_unit_vector(point_one, point_two)

        self.assertEqual(unit_vector.all(), np.array([0.7071067814, 0.7071067814]).all())

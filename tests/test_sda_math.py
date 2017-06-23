import unittest
import numpy as np
from SDA import *

class SDAVectorMathTestCase(unittest.TestCase):

    def test_multi_vector_magnitude(self):
        """
        Test the algorithm to determine the distance between two points
        """
        vector_one = np.array([0, 0])
        vector_two = np.array([10, 10])

        dist = VectorMath.get_magnitude(vector_one, vector_two)

        self.assertEqual(dist, 200**0.5)

    def test_single_vector_magnitude(self):
        """
        Test the algorithm to determine the distance between two points
        """
        vector_one = np.array([10, 10])

        dist = VectorMath.get_vector_magnitude(vector_one)

        self.assertEqual(dist, 200**0.5)

    def test_multi_unit_vector(self):
        """
        Test the algorithm to determine two points' unit vector
        """
        vector_one = np.array([0, 0])
        vector_two = np.array([10, 10])

        unit_vector = VectorMath.get_unit_vector_from_two_vectors(vector_one, vector_two)

        self.assertEqual(unit_vector.all(), np.array([0.7071067814, 0.7071067814]).all())

    def test_single_unit_vector(self):
        """
        Test the algorithm to determine two points' unit vector
        """
        vector_one = np.array([10, 10])

        unit_vector = VectorMath.get_single_unit_vector(vector_one)

        self.assertEqual(unit_vector.all(), np.array([1, 1]).all())

    def test_vector_projection(self):
        """
        Test the algorithm for vector projection
        """
        vector_one = np.array([5, 5])
        vector_two = np.array([0, 10])

        projection_vector = VectorMath.get_vector_projection(vector_one, vector_two)
        correct_projection_vector = np.array([0, 5])

        self.assertEqual(correct_projection_vector.all(), projection_vector.all())

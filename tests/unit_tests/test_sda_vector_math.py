import math
import numpy as np
import unittest
from SDA import VectorMath

class VectorMathTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_magnitude(self):

        my_vector_one = np.array([2.0, 3.0, 3.0])
        my_vector_two = np.array([6.0, 6.0, 6.0])

        self.assertEqual(VectorMath.get_magnitude(my_vector_one, my_vector_two), math.sqrt(34.0))

    def test_get_unit_vector_from_two_vectors(self):

        my_vector_one = np.array([2.0, 3.0, 3.0])
        my_vector_two = np.array([6.0, 6.0, 6.0])

        self.assertTrue(np.array_equal(VectorMath.get_unit_vector_from_two_vectors(my_vector_one, my_vector_two), np.array([4.0/math.sqrt(34.0), 3.0/math.sqrt(34.0), 3.0/math.sqrt(34.0)])))

    def test_get_single_unit_vector(self):

        my_vector = np.array([2.0, 3.0, 3.0])

        self.assertTrue(np.array_equal(VectorMath.get_single_unit_vector(my_vector), np.array([2.0/math.sqrt(22.0), 3.0/math.sqrt(22.0), 3.0/math.sqrt(22.0)])))

    def test_get_vector_magnitude(self):

        my_vector = np.array([2,0, 3.0, 3.0])

        self.assertEqual(VectorMath.get_vector_magnitude(my_vector), math.sqrt(22.0))

    def test_get_vector_projection(self):
        """
        my_vector_one = np.array([2.0, 3.0, 3.0])
        my_vector_two = np.array([6.0, 6.0, 6.0])
        """

        my_vector_three = np.array([-33.0, 0, 66.5])
        my_vector_four = np.array([0, 88.4, -32.6])

        print(VectorMath.get_vector_projection(my_vector_three, my_vector_four))
        """
        self.assertTrue(np.array_equal(VectorMath.get_vector_projection(my_vector_one, my_vector_two), np.array([8.0/3.0, 8.0/3.0, 8.0/3.0])))
        """
        self.assertTrue(np.array_equal(VectorMath.get_vector_projection(my_vector_three, my_vector_four), np.array([-0., -21.5878621, 7.96113467])))

        vector_five

    def test_get_vector_rejection(self):
        """
        my_vector_one = np.array([2.0, 3.0, 3.0])
        my_vector_two = np.array([6.0, 6.0, 6.0])
        """
        my_vector_three = np.array([-33.0, 0, 66.5])
        my_vector_four = np.array([0, 88.4, -32.6])

        print(VectorMath.get_vector_rejection(my_vector_three, my_vector_four))
        """
        self.assertTrue(np.array_equal(VectorMath.get_vector_rejection(my_vector_one, my_vector_two), np.array([-2.0/3.0, 1.0/3.0, 1.0/3.0])))
        """
        self.assertTrue(np.array_equal(VectorMath.get_vector_rejection(my_vector_three, my_vector_four), np.array([-33., 21.5878621, 58.53886533])))

import math
import numpy as np
import unittest
from SDA import VectorMath

class VectorMathTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_magnitude(self):

        my_vector1 = np.array([2.0, 3.0, 3.0])
        my_vector2 = np.array([6.0, 6.0, 6.0])

        self.assertEqual(VectorMath.get_magnitude(my_vector1, my_vector2), math.sqrt(34.0))

    def test_get_unit_vector_from_two_vectors(self):

        my_vector1 = np.array([2.0, 3.0, 3.0])
        my_vector2 = np.array([6.0, 6.0, 6.0])

        self.assertTrue(np.array_equal(VectorMath.get_unit_vector_from_two_vectors(my_vector1, my_vector2), np.array([4.0/math.sqrt(34.0), 3.0/math.sqrt(34.0), 3.0/math.sqrt(34.0)])))

    def test_get_single_unit_vector(self):

        my_vector = np.array([2.0, 3.0, 3.0])

        self.assertTrue(np.array_equal(VectorMath.get_single_unit_vector(my_vector), np.array([2.0/math.sqrt(22.0), 3.0/math.sqrt(22.0), 3.0/math.sqrt(22.0)])))

    def test_get_vector_magnitude(self):

        my_vector = np.array([2,0, 3.0, 3.0])

        self.assertEqual(VectorMath.get_vector_magnitude(my_vector), math.sqrt(22.0))

    def test_get_vector_projection(self):

        my_vector1 = np.array([2, 3, 3])
        my_vector2 = np.array([6, 6, 6])

        my_vector3 = np.array([-33.0, 0, 66.5])
        my_vector4 = np.array([0, 88.4, -32.6])

        my_vector5 = np.array([1,2,3])
        my_vector6 = np.array([-3,-2,-1])

        print(VectorMath.get_vector_projection(my_vector1, my_vector2))
        print(VectorMath.get_vector_projection(my_vector3, my_vector4))
        print(VectorMath.get_vector_projection(my_vector5, my_vector6))

        self.assertTrue(np.array_equal(np.round(VectorMath.get_vector_projection(my_vector1, my_vector2), decimals = 5, out = None), np.round(np.array([8.0/3.0, 8.0/3.0, 8.0/3.0]), decimals = 5, out = None)))
        self.assertTrue(np.array_equal(np.round(VectorMath.get_vector_projection(my_vector3, my_vector4), decimals = 5, out = None), np.round(np.array([-0., -21.5878621, 7.96113467]), decimals = 5, out = None)))
        self.assertTrue(np.array_equal(np.round(VectorMath.get_vector_projection(my_vector5, my_vector6), decimals = 5, out = None), np.round(np.array([15.0/7.0, 10.0/7.0, 5.0/7.0]), decimals = 5, out = None)))

    def test_get_vector_rejection(self):

        my_vector1 = np.array([2, 3, 3])
        my_vector2 = np.array([6, 6, 6])

        my_vector3 = np.array([-33.0, 0, 66.5])
        my_vector4 = np.array([0, 88.4, -32.6])

        my_vector5 = np.array([1,2,3])
        my_vector6 = np.array([-3,-2,-1])

        print(VectorMath.get_vector_rejection(my_vector1, my_vector2))
        print(VectorMath.get_vector_rejection(my_vector3, my_vector4))
        print(VectorMath.get_vector_rejection(my_vector5, my_vector6))

        self.assertTrue(np.array_equal(np.round(VectorMath.get_vector_rejection(my_vector1, my_vector2), decimals = 5, out = None), np.round(np.array([-2.0/3.0, 1.0/3.0, 1.0/3.0]), decimals = 5, out = None)))
        self.assertTrue(np.array_equal(np.round(VectorMath.get_vector_rejection(my_vector3, my_vector4), decimals = 5, out = None), np.round(np.array([-33, 21.5878621, 58.53886533]), decimals = 5, out = None)))
        self.assertTrue(np.array_equal(np.round(VectorMath.get_vector_rejection(my_vector5, my_vector6), decimals = 5, out = None), np.round(np.array([-8.0/7.0, 4.0/7.0, 16.0/7.0]), decimals = 5, out = None)))

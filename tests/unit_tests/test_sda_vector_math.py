import math
import numpy
import unittest
from SDA import VectorMath

class VectorMathTestCase(unittest.TestCase):

    def test_get_magnitude(self):

        test_vector1 = numpy.array([2.0, 3.0, 3.0])
        test_vector2 = numpy.array([6.0, 6.0, 6.0])

        self.assertEqual(VectorMath.get_magnitude(test_vector1, test_vector2), math.sqrt(34.0))

    def test_get_unit_vector_from_two_vectors(self):

        test_vector1 = numpy.array([2.0, 3.0, 3.0])
        test_vector2 = numpy.array([6.0, 6.0, 6.0])

        self.assertTrue(numpy.array_equal(VectorMath.get_unit_vector_from_two_vectors(test_vector1, test_vector2), numpy.array([4.0/math.sqrt(34.0), 3.0/math.sqrt(34.0), 3.0/math.sqrt(34.0)])))

    def test_get_single_unit_vector(self):

        test_vector = numpy.array([2.0, 3.0, 3.0])

        self.assertTrue(numpy.array_equal(VectorMath.get_single_unit_vector(test_vector), numpy.array([2.0/math.sqrt(22.0), 3.0/math.sqrt(22.0), 3.0/math.sqrt(22.0)])))

    def test_get_vector_magnitude(self):

        test_vector = numpy.array([2,0, 3.0, 3.0])

        self.assertEqual(VectorMath.get_vector_magnitude(test_vector), math.sqrt(22.0))

    def test_get_vector_projection(self):

        test_vector1 = numpy.array([2, 3, 3])
        test_vector2 = numpy.array([6, 6, 6])

        test_vector3 = numpy.array([-33.0, 0, 66.5])
        test_vector4 = numpy.array([0, 88.4, -32.6])

        test_vector5 = numpy.array([1,2,3])
        test_vector6 = numpy.array([-3,-2,-1])

        print(VectorMath.get_vector_projection(test_vector1, test_vector2))
        print(VectorMath.get_vector_projection(test_vector3, test_vector4))
        print(VectorMath.get_vector_projection(test_vector5, test_vector6))

        self.assertTrue(numpy.array_equal(numpy.round(VectorMath.get_vector_projection(test_vector1, test_vector2), decimals = 5, out = None), numpy.round(numpy.array([8.0/3.0, 8.0/3.0, 8.0/3.0]), decimals = 5, out = None)))
        self.assertTrue(numpy.array_equal(numpy.round(VectorMath.get_vector_projection(test_vector3, test_vector4), decimals = 5, out = None), numpy.round(numpy.array([-0., -21.5878621, 7.96113467]), decimals = 5, out = None)))
        self.assertTrue(numpy.array_equal(numpy.round(VectorMath.get_vector_projection(test_vector5, test_vector6), decimals = 5, out = None), numpy.round(numpy.array([15.0/7.0, 10.0/7.0, 5.0/7.0]), decimals = 5, out = None)))

    def test_get_vector_rejection(self):

        test_vector1 = numpy.array([2, 3, 3])
        test_vector2 = numpy.array([6, 6, 6])

        test_vector3 = numpy.array([-33.0, 0, 66.5])
        test_vector4 = numpy.array([0, 88.4, -32.6])

        test_vector5 = numpy.array([1,2,3])
        test_vector6 = numpy.array([-3,-2,-1])

        print(VectorMath.get_vector_rejection(test_vector1, test_vector2))
        print(VectorMath.get_vector_rejection(test_vector3, test_vector4))
        print(VectorMath.get_vector_rejection(test_vector5, test_vector6))

        self.assertTrue(numpy.array_equal(numpy.round(VectorMath.get_vector_rejection(test_vector1, test_vector2), decimals = 5, out = None), numpy.round(numpy.array([-2.0/3.0, 1.0/3.0, 1.0/3.0]), decimals = 5, out = None)))
        self.assertTrue(numpy.array_equal(numpy.round(VectorMath.get_vector_rejection(test_vector3, test_vector4), decimals = 5, out = None), numpy.round(numpy.array([-33, 21.5878621, 58.53886533]), decimals = 5, out = None)))
        self.assertTrue(numpy.array_equal(numpy.round(VectorMath.get_vector_rejection(test_vector5, test_vector6), decimals = 5, out = None), numpy.round(numpy.array([-8.0/7.0, 4.0/7.0, 16.0/7.0]), decimals = 5, out = None)))

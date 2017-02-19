import unittest
from ObjAvoidSimplified import *

class RandomPointMakerTestCase(unittest.TestCase):

    def test_random_point_maker(self):
        """
        Test the random point maker to ensure it makes random points
        of specific dimensions and within specified bounds
        """
        dimensions = 2
        num_points = 5
        bounds = ((0, 10), (0, 10))

        random_points = get_random_points_in_bounds(dimensions, num_points, bounds)

        self.assertEqual(len(random_points), num_points)

        for point in random_points:
            for dim in range(dimensions):
                self.assertTrue(point[dim] >= bounds[dim][0])
                self.assertTrue(point[dim] <= bounds[dim][1])

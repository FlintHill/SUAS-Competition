import unittest
import numpy as np
from SDA import *

class SDA2TestCase(unittest.TestCase):

    def test_obstacle_avoidance_with_boundaries(self):
        """
        Test the obstacle map to determine
        """
        flight_boundary_points = np.array([np.array([[-10, -10], [250, -10], [250, 250], [-10, 250]])])
        obstacle_map = ObstacleMap(np.array([0,0,0]), flight_boundary_points)
        test_obstacle = StationaryObstacle(np.array([100, 0, 0]), 50, 500)
        waypoint = np.array([200, 0, 0])

        obstacle_map.add_obstacle(np.array([test_obstacle]))
        obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_paths = obstacle_map.is_obstacle_in_path()
        self.assertTrue(obstacle_in_path_boolean)

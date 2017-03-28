import unittest
import numpy as np
from SDA import *

class SDATestCase(unittest.TestCase):

    def setUp(self):
        self.obstacle_map = ObstacleMap()

    def test_add_obstacles(self):
        """
        Test ObstacleMap's add_obstacle() method
        """
        new_obstacle = StationaryObstacle(np.array([0, 10]), 5)

        self.obstacle_map.add_obstacle(np.array([new_obstacle]))

        self.assertEqual(self.obstacle_map.get_obstacles().size, 1)

    def test_reset_obstacles(self):
        """
        Test ObstacleMap's reset_obstacles() method
        """
        new_obstacle = StationaryObstacle(np.array([0, 10]), 5)

        self.obstacle_map.add_obstacle(np.array([new_obstacle]))
        self.obstacle_map.reset_obstacles()

        self.assertEqual(self.obstacle_map.get_obstacles().size, 0)

    def test_reset_waypoints(self):
        """
        Test ObstacleMap's reset_waypoints() method
        """
        self.obstacle_map.reset_obstacles()
        waypoint = np.array([20, 0])

        self.obstacle_map.add_waypoint(waypoint)

        self.obstacle_map.reset_waypoints()
        self.assertEqual(len(self.obstacle_map.get_drone().get_waypoint_holder()), 0)

    def test_is_obstacle_in_path(self):
        """
        Test ObstacleMap's is_obstacle_in_path() function
        """
        # First intersection test
        self.obstacle_map.reset_obstacles()
        obstacle_in_path = StationaryObstacle(np.array([20, 0]), 5)
        waypoint = np.array([40, 0])

        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()
        self.assertEqual(obstacle_in_path_boolean, True)
        self.assertEqual(np.array_equal(avoid_coords[0], np.array([20, -20])), True)
        self.assertEqual(np.array_equal(avoid_coords[1], np.array([20, 20])), True)

        # Second intersection test
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        obstacle_in_path = StationaryObstacle(np.array([20, 20]), 5)
        waypoint = np.array([0, 40])

        self.obstacle_map.set_drone_position(np.array([0, 0]))
        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()

        self.assertEqual(obstacle_in_path_boolean, False)
        self.assertEqual(avoid_coords, None)

        # Third intersection test
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        obstacle_in_path = StationaryObstacle(np.array([30, 30]), 5)
        waypoint = np.array([60, 60])

        self.obstacle_map.set_drone_position(np.array([0, 0]))
        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()

        self.assertEqual(obstacle_in_path_boolean, True)

        # Fourth intersection test
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        obstacle_in_path = StationaryObstacle(np.array([20, 20]), 5)
        waypoint = np.array([60, 60])

        self.obstacle_map.set_drone_position(np.array([40, 40]))
        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()

        self.assertEqual(obstacle_in_path_boolean, False)
        self.assertEqual(avoid_coords, None)

    def test_get_min_path(self):
        """
        Test ObstacleMap's get_min_path method
        """
        # Fourth intersection test
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        obstacle_in_path = StationaryObstacle(np.array([20, 0]), 5)
        waypoint = np.array([0, 20])

        self.obstacle_map.set_drone_position(np.array([0, 0]))
        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()
        #min_tangent_point = self.obstacle_map.get_min_tangent_point(avoid_coords)

        self.assertEqual(obstacle_in_path_boolean, False)

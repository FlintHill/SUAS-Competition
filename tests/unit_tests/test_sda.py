import unittest
import numpy as np
from SDA import *

class SDATestCase(unittest.TestCase):

    def setUp(self):
        self.obstacle_map = ObstacleMap(np.array([0,0,0]), np.array([np.array([[-2000, -2000], [-2000, 2000], [2000, 2000], [2000, -2000]])]))

    def test_add_obstacles(self):
        """
        Test ObstacleMap's add_obstacle() method
        """
        new_obstacle = StationaryObstacle(np.array([0, 10, 0]), 5, 20)

        self.obstacle_map.add_obstacle(new_obstacle)

        self.assertEqual(self.obstacle_map.get_obstacles().size, 1)

    def test_reset_obstacles(self):
        """
        Test ObstacleMap's reset_obstacles() method
        """
        new_obstacle = StationaryObstacle(np.array([0, 10, 0]), 5, 20)

        self.obstacle_map.add_obstacle(new_obstacle)
        self.obstacle_map.reset_obstacles()

        self.assertEqual(self.obstacle_map.get_obstacles().size, 0)

    def test_reset_waypoints(self):
        """
        Test ObstacleMap's reset_waypoints() method
        """
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.set_drone_position(np.array([0,0,0]))
        waypoint = np.array([20, 0, 0])

        self.obstacle_map.add_waypoint(waypoint)

        self.obstacle_map.reset_waypoints()
        self.assertEqual(len(self.obstacle_map.get_drone().get_waypoint_holder()), 0)

    def test_obstacle_in_path_detection_false(self):
        """
        Test ObstacleMap's ability to determine if obstacles intersect with
        waypoint path. This test includes an obstacle that is not in the path
        of the UAV.
        """
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        self.obstacle_map.set_drone_position(np.array([0,0,0]))
        obstacle_in_path = StationaryObstacle(np.array([50, 0, 0]), 5, 20)
        waypoint = np.array([50, 50, 0])

        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_paths = self.obstacle_map.is_obstacle_in_path()
        self.assertEqual(obstacle_in_path_boolean, False)

    def test_obstacle_in_path_detection_true(self):
        """
        Test ObstacleMap's ability to determine if obstacles intersect with
        waypoint path. This test includes an obstacle that is in the path of
        the UAV.
        """
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        self.obstacle_map.set_drone_position(np.array([0,0,0]))
        obstacle_in_path = StationaryObstacle(np.array([50, 0, 0]), 5, 20)
        waypoint = np.array([100, 0, 0])

        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_paths = self.obstacle_map.is_obstacle_in_path()
        self.assertEqual(obstacle_in_path_boolean, True)

    def test_obstacle_under_waypoint_path_false(self):
        """
        Test ObstacleMap's ability to go above an obstacle
        """
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        self.obstacle_map.set_drone_position(np.array([0,0,0]))
        obstacle_in_path = StationaryObstacle(np.array([50, 0, 0]), 5, 10)
        waypoint = np.array([100, 0, 50])
        new_uav_position = np.array([0, 0, 50])

        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)
        self.obstacle_map.set_drone_position(new_uav_position)

        obstacle_in_path_boolean, avoid_paths = self.obstacle_map.is_obstacle_in_path()
        self.assertEqual(obstacle_in_path_boolean, False)

    def test_obstacle_under_waypoint_path_true(self):
        """
        Test ObstacleMap's ability to go above an obstacle
        """
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        self.obstacle_map.set_drone_position(np.array([0,0,0]))
        obstacle_in_path = StationaryObstacle(np.array([50, 0, 0]), 5, 15)
        waypoint = np.array([100, 0, 25])
        new_uav_position = np.array([0, 0, 25])

        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_waypoint(waypoint)
        self.obstacle_map.set_drone_position(new_uav_position)

        obstacle_in_path_boolean, avoid_paths = self.obstacle_map.is_obstacle_in_path()
        self.assertEqual(obstacle_in_path_boolean, True)

    def test_obstacle_avoid_coords_1(self):
        """
        Test ObstacleMap's ability to generate correct avoidance coordinates
        """
        self.obstacle_map.reset_obstacles()
        self.obstacle_map.reset_waypoints()
        self.obstacle_map.set_drone_position(np.array([0,0,0]))
        obstacle_in_path = StationaryObstacle(np.array([-837.24189827,700.1041422,500]), 150, 500)
        waypoint = np.array([-1027.15210095,168.51612707,200.0000034 ])
        new_uav_position = np.array(np.array([-668.95868657,1051.56233827,200.0000064]))

        self.obstacle_map.add_obstacle(obstacle_in_path)
        self.obstacle_map.add_obstacle(StationaryObstacle(np.array([0,0,0]), 150, 500))
        self.obstacle_map.add_waypoint(waypoint)
        self.obstacle_map.set_drone_position(new_uav_position)

        obstacle_in_path_boolean, avoid_paths = self.obstacle_map.is_obstacle_in_path()
        self.assertEqual(obstacle_in_path_boolean, False)

    def test_flight_boundary_simple(self):
        """
        Test the flight boundary system using a simple boundary
        """
        min_alt = 100
        max_alt = 750
        flight_boundary_test_object = FlightBoundary(min_alt, max_alt, np.array([[-2000, -2000], [-2000, 2000], [2000, 2000], [2000, -2000]]))

        # Inside alt
        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([0, 0, ((min_alt + max_alt) / 2)]))
        self.assertTrue(in_bounds_boolean)

        # Below minimum altitude
        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([0, 0, min_alt - 10]))
        self.assertEqual(in_bounds_boolean, False)

        # Above maximum altitude
        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([0, 0, max_alt + 10]))
        self.assertEqual(in_bounds_boolean, False)

        # Inside alt, outside XY
        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([2010, 2010, ((min_alt + max_alt) / 2)]))
        self.assertEqual(in_bounds_boolean, False)

    def test_flight_boundary_complicated(self):
        """
        Test the flight boundary system using a complicated boundary
        """
        min_alt = 100
        max_alt = 750
        flight_boundary_test_object = FlightBoundary(min_alt, max_alt, np.array([[0, 1000], [100, 100], [1000, 0], [100, -100], [0, -1000], [-100, -100], [-1000, 0], [-100, 100]]))

        # Inside bounds
        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([50, 50, 200]))
        self.assertTrue(in_bounds_boolean)

        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([0, 800, 200]))
        self.assertTrue(in_bounds_boolean)

        # Outside bounds
        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([200, 200, 200]))
        self.assertEqual(in_bounds_boolean, False)

        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([-200, -200, 200]))
        self.assertEqual(in_bounds_boolean, False)

        in_bounds_boolean = flight_boundary_test_object.is_point_in_bounds(np.array([0, 2000, 200]))
        self.assertEqual(in_bounds_boolean, False)

    def test_obstacle_avoidance_with_boundaries(self):
        """
        Test the obstacle map to determine
        """
        flight_boundary_points = np.array([np.array([[-10, -10], [250, -10], [250, 250], [-10, 250]])])
        obstacle_map = ObstacleMap(np.array([0,0,0]), flight_boundary_points)
        test_obstacle = StationaryObstacle(np.array([100, 0, 0]), 50, 500)
        waypoint = np.array([200, 0, 0])

        obstacle_map.add_obstacle(test_obstacle)
        obstacle_map.add_waypoint(waypoint)

        obstacle_in_path_boolean, avoid_paths = obstacle_map.is_obstacle_in_path()
        self.assertTrue(obstacle_in_path_boolean)

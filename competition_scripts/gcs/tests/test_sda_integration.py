from static_math import *
from gps_coordinates import GPSCoordinates
from SDA import *
from updated_client_converter_test import ClientConverter
from waypoint import Waypoint
import unittest
import numpy as np

class SDAIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        """
        Initialize
        """
        self.setup_client_converter()

    def setup_client_converter(self):
        self.initial_coordinates = GPSCoordinates(38.8703041, -77.3214035, 60.950000762939453)

        self.client_converter = ClientConverter(self.initial_coordinates)

    def test_get_initial_coordinates(self):
        """
        Test the get_initial_coordinates() method
        """
        initial_coordinates = self.client_converter.get_initial_coordinates()

        self.assertEqual(self.initial_coordinates.get_latitude(), initial_coordinates.get_latitude())
        self.assertEqual(self.initial_coordinates.get_longitude(), initial_coordinates.get_longitude())
        self.assertEqual(self.initial_coordinates.get_altitude(), initial_coordinates.get_altitude())

    def test_reset_obstacles(self):
        """
        Test the reset_obstacles() method
        """
        new_obstacle = GPSCoordinates(38.8703041, -77.3214035, 60.950000762939453)
        self.client_converter.add_obstacle(new_obstacle)
        obstacle_map = self.client_converter.get_obstacle_map()

        self.assertEqual(obstacle_map.obstacles.size, 1)

        self.client_converter.reset_obstacles()
        obstacle_map = self.client_converter.get_obstacle_map()

        self.assertEqual(obstacle_map.obstacles.size, 0)

    def test_set_waypoints(self):
        """
        Test the set_waypoints() method
        """
        test_waypoint = Waypoint(38.8742103, -77.3217697, 91.44000244140625)
        self.client_converter.set_waypoints([test_waypoint])
        obstacle_map = self.client_converter.get_obstacle_map()
        waypoint_holder = obstacle_map.drone.get_waypoint_holder()
        new_gps_point = inverse_haversine(self.client_converter.get_initial_coordinates(),
            float((waypoint_holder[0][0]**2.0 + waypoint_holder[0][1]**2)**0.5), 0, -0.0728563478644)

        self.assertTrue(abs(new_gps_point.get_latitude() - test_waypoint.get_latitude()) < 0.0000002)
        self.assertTrue(abs(new_gps_point.get_longitude() - test_waypoint.get_longitude()) < 0.0000002)

    def test_update_drone_mass_position(self):
        """
        Test the update_drone_mass_position() method
        """
        self.setup_client_converter()

        test_waypoint = Waypoint(38.8742103, -77.3217697, 91.44000244140625)
        self.client_converter.set_waypoints([test_waypoint])
        waypoint_holder = self.client_converter.obstacle_map.drone.get_waypoint_holder()
        self.client_converter.obstacle_map.add_obstacle(StationaryObstacle(np.array([waypoint_holder[0][0] / 2.0, waypoint_holder[0][1] / 2.0]), 50))
        new_geo_point, map_point = self.client_converter.update_drone_mass_position(None)

        self.assertTrue(abs(new_geo_point.get_latitude() - 38.8722212663) < 0.0000001)
        self.assertTrue(abs(new_geo_point.get_longitude() + 77.3222201905) < 0.0000001)

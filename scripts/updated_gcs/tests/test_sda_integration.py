from math_functions import *
from converter_functions import *
from SDA import *
from sda_converter import SDAConverter
from location_data import *
import unittest
import numpy

class SDAIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        """
        Initialize
        """
        self.setup_client_converter()

    def setup_client_converter(self):
        self.initial_coordinates = Location(38.8703041, -77.3214035, 60.950000762939453)

        self.client_converter = SDAConverter(self.initial_coordinates)

    def test_reset_obstacles(self):
        """
        Test the reset_obstacles() method
        """
        new_obstacle = Location(38.8703041, -77.3214035, 60.950000762939453)
        self.client_converter.add_obstacle(new_obstacle, new_obstacle)
        obstacle_map = self.client_converter.obstacle_map

        self.assertEqual(obstacle_map.obstacles.size, 1)

        self.client_converter.reset_obstacles()
        obstacle_map = self.client_converter.obstacle_map

        self.assertEqual(obstacle_map.obstacles.size, 0)

    def test_set_waypoints(self):
        """
        Test the set_waypoints() method
        """
        test_waypoint = Location(38.8742103, -77.3217697, 91.44000244140625)
        self.client_converter.set_waypoint(test_waypoint)
        obstacle_map = self.client_converter.obstacle_map
        waypoint_holder = obstacle_map.drone.get_waypoint_holder()
        new_gps_point = inverse_haversine(self.client_converter.initial_coordinates,
            [waypoint_holder[0][0], waypoint_holder[0][1], 91.44000244140625], -0.0728563478644)

        self.assertTrue(abs(new_gps_point.get_lat() - test_waypoint.get_lat()) < 0.00002)
        self.assertTrue(abs(new_gps_point.get_lon() - test_waypoint.get_lon()) < 0.00002)

    def test_update_drone_mass_position(self):
        """
        Test the update_drone_mass_position() method
        """
        self.setup_client_converter()

        test_waypoint = Location(38.8742103, -77.3217697, 91.44000244140625)
        self.client_converter.set_waypoint(test_waypoint)
        waypoint_holder = self.client_converter.obstacle_map.drone.get_waypoint_holder()
        self.client_converter.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([waypoint_holder[0][0] / 2.0, waypoint_holder[0][1] / 2.0]), 50))
        uav_bearing = bearing(self.initial_coordinates, test_waypoint)
        new_geo_point = self.client_converter.avoid_obstacles(uav_bearing)

        print(new_geo_point.lat)
        print(new_geo_point.lon)
        self.assertTrue(abs(new_geo_point.lat - 38.8717414325) < 0.0000001)
        self.assertTrue(abs(new_geo_point.lon + 77.3232347661) < 0.0000001)

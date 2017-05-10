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
        self.boundary_points = [
            Location(38.867580, -77.330360, 0),
            Location(38.876535, -77.330060, 0),
            Location(38.877002, -77.314997, 0),
            Location(38.867513, -77.315769, 0)
        ]

        self.sda_converter = SDAConverter(self.initial_coordinates, self.boundary_points)

    def test_reset_obstacles(self):
        """
        Test the reset_obstacles() method
        """
        new_obstacle = Location(38.8703041, -77.3214035, 60.950000762939453)
        self.sda_converter.add_obstacle(new_obstacle, new_obstacle)
        obstacle_map = self.sda_converter.obstacle_map

        self.assertEqual(obstacle_map.obstacles.size, 1)

        self.sda_converter.reset_obstacles()
        obstacle_map = self.sda_converter.obstacle_map

        self.assertEqual(obstacle_map.obstacles.size, 0)

    def test_set_waypoints(self):
        """
        Test the set_waypoints() method
        """
        test_waypoint = Location(38.8742103, -77.3217697, 91.44000244140625)
        self.sda_converter.set_waypoint(test_waypoint)
        obstacle_map = self.sda_converter.obstacle_map
        waypoint_holder = obstacle_map.drone.get_waypoint_holder()
        new_gps_point = inverse_haversine(self.sda_converter.initial_coordinates,
            [waypoint_holder[0][0], waypoint_holder[0][1], 91.44000244140625])

        self.assertTrue(abs(new_gps_point.get_lat() - test_waypoint.get_lat()) < 0.004)
        self.assertTrue(abs(new_gps_point.get_lon() - test_waypoint.get_lon()) < 0.004)

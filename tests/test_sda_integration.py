from SUASSystem import *
from SDA import *
import unittest
import numpy
import interop

class SDAIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        """
        Initialize
        """
        self.setup_client_converter()

    def setup_client_converter(self):
        self.initial_coordinates = Location(38.8703041, -77.3214035, 60.950000762939453)
        self.boundary_points = [
            {
                "boundary_pts" : [
                    {"latitude" : 38.867580, "longitude" : -77.330360, "order" : 0},
                    {"latitude" : 38.876535, "longitude" : -77.330060, "order" : 0},
                    {"latitude" : 38.877002, "longitude" : -77.314997, "order" : 0},
                    {"latitude" : 38.867513, "longitude" : -77.315769, "order" : 0}
                ]
            }
        ]

        self.sda_converter = SDAConverter(self.initial_coordinates, numpy.array([self.boundary_points]))

    def test_reset_obstacles(self):
        """
        Test the reset_obstacles() method
        """
        new_obstacle = interop.StationaryObstacle(38.8703041, -77.3214035, 0, 60.950000762939453)
        self.sda_converter.add_obstacle(Location(38.8703041, -77.3214035, 60.950000762939453), new_obstacle)
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

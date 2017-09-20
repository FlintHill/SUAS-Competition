import numpy as np
from SDA import WaypointHolder
from SUASSystem import *
import unittest

class DroneTestCase(unittest.TestCase):

    def setUp(self):
        self.drone = Drone(np.array([0,0,0]), np.array([[ 7, 10, 13], [21, 24, 27]]))

    def test_set_drone_pos(self):
        self.drone.set_drone_position(np.array([1,1,1]))
        self.assertEquals(np.array([1,1,1]).any(), self.drone.point.any())

    def test_add_waypoint(self):
        self.drone.add_waypoint(np.array([20,20,20]))
        self.assertEquals(np.array([[ 7, 10, 13], [21, 24, 27], [20, 20, 20]]).any(), self.drone.waypoint_holder.waypoints.any())

    def test_reset_waypoints(self):
        self.drone.reset_waypoints()
        self.assertEquals(0, self.drone.waypoint_holder.waypoints.shape[0])

    def test_has_reached_waypoint(self):
        self.drone = Drone(np.array([0,0,0]), np.array([[ 7, 10, 13], [21, 24, 27]]))
        self.assertFalse(self.drone.has_reached_waypoint())

    def test_get_point(self):
        self.assertEquals(np.array([0,0,0]).all(), self.drone.get_point().all())

    def test_get_waypoint_holder(self):
        self.assertEquals(np.array([[ 7, 10, 13], [21, 24, 27]]).any(), self.drone.get_waypoint_holder().waypoints.any())

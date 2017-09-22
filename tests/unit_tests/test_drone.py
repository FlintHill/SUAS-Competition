import numpy
from SDA import WaypointHolder
from SUASSystem import *
import unittest

class DroneTestCase(unittest.TestCase):

    def setUp(self):
        self.drone = Drone(numpy.array([0,0,0]), numpy.array([[ 7, 10, 13], [21, 24, 27]]))

    def test_set_drone_pos(self):
        self.drone.set_drone_position(numpy.array([1,1,1]))
        self.assertTrue(numpy.array_equal(numpy.array([1,1,1]), self.drone.point))

    def test_add_waypoint(self):
        self.drone.reset_waypoints()
        self.drone.add_waypoint(numpy.array([20,20,20]))
        self.assertTrue(numpy.array_equal(numpy.array([20, 20, 20]), self.drone.waypoint_holder.waypoints[0]))
        self.drone.add_waypoint(numpy.array([10,10,10]))
        self.assertTrue(numpy.array_equal(numpy.array([[20, 20, 20], [10, 10, 10]]), self.drone.waypoint_holder.waypoints))

    def test_reset_waypoints(self):
        self.drone.reset_waypoints()
        self.assertTrue(numpy.array_equal(numpy.array([]), self.drone.waypoint_holder.waypoints))

    def test_has_reached_waypoint(self):
        self.drone.reset_waypoints()
        self.drone.add_waypoint(numpy.array([21,24,27]))
        self.assertFalse(self.drone.has_reached_waypoint())
        self.drone.set_drone_position(numpy.array([21,24,27]))
        self.assertTrue(self.drone.has_reached_waypoint())


    def test_get_point(self):
        self.drone.set_drone_position(numpy.array([0,0,0]))
        self.assertTrue(numpy.array_equal(numpy.array([0,0,0]), self.drone.get_point()))

    def test_get_waypoint_holder(self):
        self.drone.reset_waypoints()
        self.drone.add_waypoint(numpy.array([20,20,20]))
        self.assertTrue(numpy.array_equal(numpy.array([[20, 20, 20]]), self.drone.get_waypoint_holder().waypoints))

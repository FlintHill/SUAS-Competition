import unittest
from SDA import *
import numpy

class TestSDADrone(unittest.TestCase):

    def setUp(self):
        self.initial_drone_point = numpy.array([0,0,0])
        self.first_waypoints = numpy.array([[1,2,3], [4,5,6]])

    def test_set_drone_position(self):
        test_drone_position = numpy.array([1,1,1])
        test_drone = Drone(self.initial_drone_point, self.first_waypoints)

        test_drone.set_drone_position(test_drone_position)
        self.assertEqual(test_drone.point[2], test_drone_position[2])

    def test_add_waypoint(self):
        new_waypoint = numpy.array([7,8,9])
        test_drone= Drone(self.initial_drone_point, self.first_waypoints)

        test_drone.add_waypoint(new_waypoint)
        self.assertEqual(test_drone.waypoint_holder.waypoints[2][2], new_waypoint[2])

    def test_reset_waypoints(self):
        test_drone= Drone(self.initial_drone_point, self.first_waypoints)

        test_drone.reset_waypoints()
        self.assertEqual(test_drone.waypoint_holder.waypoints.size, 0)

    def test_has_reached_waypoint(self):
        close_point = numpy.array([1,2,3])
        far_point = numpy.array([100,100,-100])

        test_drone= Drone(far_point, self.first_waypoints)
        self.assertFalse(test_drone.has_reached_waypoint())

        test_drone= Drone(close_point, self.first_waypoints)
        self.assertTrue(test_drone.has_reached_waypoint())

    def test_get_point(self):
        test_point = numpy.array([0,0,156])
        test_drone= Drone(test_point, self.first_waypoints)

        self.assertEqual(test_drone.get_point()[2], test_point[2])

    def test_get_waypoint_holder(self):
        test_drone= Drone(self.initial_drone_point, self.first_waypoints)

        self.assertEqual(test_drone.get_waypoint_holder().waypoints[1][2], self.first_waypoints[1][2])

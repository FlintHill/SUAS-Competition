import unittest
from SDA import *
import numpy

class TestSDAWaypoinHolder(unittest.TestCase):

    def setUp(self):
        self.waypoints = numpy.array([[1,2,3],[4,5,6]]) #Must remain a 2D array

    def test_add_waypoint(self):
        single_waypoint = numpy.array([7,8,9])
        test_waypoint_holder = WaypointHolder(self.waypoints)

        test_waypoint_holder.add_waypoint(single_waypoint)
        self.assertEqual(len(test_waypoint_holder.waypoints), len(self.waypoints) + 1)

    def test_add_empty_waypoint(self):
        empty_waypoint = numpy.array([])
        single_waypoint = numpy.array([7,8,9])
        test_waypoint_holder = WaypointHolder(empty_waypoint)

        test_waypoint_holder.add_waypoint(single_waypoint)
        self.assertEqual(test_waypoint_holder.waypoints[0][2], single_waypoint[2])

    def test_get_current_waypoint(self):
        test_waypoint_holder = WaypointHolder(self.waypoints)
        self.assertTrue(numpy.array_equal(test_waypoint_holder.get_current_waypoint(), self.waypoints[0]))

    def test_reached_any_waypoint(self):
        far_point = numpy.array([10,11,12])
        close_point = numpy.array([1,2,3])
        distance_to_target = 3

        test_waypoint_holder = WaypointHolder(self.waypoints)
        self.assertFalse(test_waypoint_holder.reached_any_waypoint(far_point, distance_to_target))

        test_waypoint_holder = WaypointHolder(self.waypoints)
        self.assertTrue(test_waypoint_holder.reached_any_waypoint(close_point, distance_to_target))

    def test_reached_current_waypoint(self):
        test_waypoint_holder = WaypointHolder(self.waypoints)

        self.assertTrue(test_waypoint_holder.reached_current_waypoint(self.waypoints[0]))
        self.assertTrue(test_waypoint_holder.reached_current_waypoint(self.waypoints[1]))

import numpy as np
from SDA import WaypointHolder

class Drone(object):
    """
    Wrapper for drone
    """

    def __init__(self, point, waypoints):
        """
        :param point: The starting point of the drone
        :type point: Numpy Array
        :param waypoints: The waypoints for the drone
        :type waypoints: Numpy Array
        """
        self.waypoint_holder = WaypointHolder(waypoints)
        self.point = point

    def set_drone_position(self, new_point):
        """
        Update the drone's position and update the waypoint holder

        :param new_point: New point for the drone
        :type new_point: Numpy Array
        """
        self.point = new_point

        self.waypoint_holder.reached_current_waypoint(self.point)

    def add_waypoint(self, waypoint):
        """
        Add a waypoint to the WaypointHolder

        :param waypoint: Waypoint to add
        :type waypoint: Numpy Array
        """
        self.waypoint_holder.add_waypoint(waypoint)

    def reset_waypoints(self):
        """
        Reset the waypoint holder
        """
        self.waypoint_holder = WaypointHolder(np.array([]))

    def has_reached_waypoint(self):
        """
        Return True if the drone has hit the current waypoint
        """
        return self.waypoint_holder.reached_current_waypoint(self.point)

    def get_point(self):
        """
        Return point
        """
        return self.point

    def get_waypoint_holder(self):
        """
        Return the waypoint holder
        """
        return self.waypoint_holder

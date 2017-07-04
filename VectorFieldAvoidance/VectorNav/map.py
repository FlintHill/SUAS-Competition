import numpy as np
from math import atan2, cos, sin, pi
from VectorNav import *

class Map(object):
    """
    Wrapper class for a map
    """

    def __init__(self, drone_point, fly_zones):
        """
        Initialize

        :param drone_point: The UAV's starting location
        :type drone_point: Numpy Array
        :param fly_zones: The fly zones for the UAV
        :type fly_zones: Numpy Array
        """
        self.obstacles = np.array([])
        self.drone = Drone(drone_point, np.array([]))
        self.flight_boundary = FlightBoundariesContainer(fly_zones)

    def add_obstacle(self, obstacle_to_add):
        """
        Add an obstacle to the map

        :param obstacle_to_add: The obstacle to add to the map
        :type obstacle_to_add: StationaryObstacle
        """
        if self.obstacles.size != 0:
            self.obstacles = np.hstack((self.obstacles, obstacle_to_add))
        else:
            self.obstacles = np.array([obstacle_to_add])

    def add_waypoint(self, waypoint):
        """
        Add a waypoint to the drone

        :param waypoint: The waypoint to add
        :type waypoint: Numpy Array
        """
        self.drone.add_waypoint(waypoint)

    def set_drone_position(self, new_point):
        """
        Set the drone's location in the map

        :param new_point: The new point for the drone
        :type new_point: Numpy Array
        """
        self.drone.set_drone_position(new_point)

    def reset_obstacles(self):
        """
        Reset the obstacles' positions within the map (should be called
        when map is refreshed to clean the array)
        """
        self.obstacles = np.array([])

    def reset_waypoints(self):
        """
        Reset the waypoints
        """
        self.drone.reset_waypoints()

    def is_obstacle_in_path(self):
        """
        Return True if drone should avoid obstacle and False if not
        """
        return False, None

    def get_obstacles(self):
        """
        Return the obstacles in the map
        """
        return self.obstacles

    def has_uav_reached_current_waypoint(self):
        """
        Return True if the UAV has reached the current waypoint and false if not
        """
        return self.drone.has_reached_waypoint()

    def get_drone(self):
        """
        Return the drone
        """
        return self.drone

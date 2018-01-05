import numpy as np
from SDAWithVectorField import VectorMath
from SDAWithVectorField import Constants

class WaypointHolder(object):

    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.waypoint_index = 0

    def add_waypoint(self, waypoint):
        if self.waypoints.size == 0:
            self.waypoints = np.array([waypoint])
        else:
            self.waypoints = np.vstack([self.waypoints, waypoint])

    def get_current_waypoint(self):
        return self.waypoints[self.waypoint_index]

    def reached_current_waypoint(self, drone_point):
        """
        Return True if the drone mass has reached the current waypoint

        :param drone_point: The drone's current position
        """
        reached_waypoint = False
        if self.waypoint_index < len(self.waypoints):
            reached_waypoint = VectorMath.get_magnitude(drone_point, self.waypoints[self.waypoint_index]) < Constants.MAX_DISTANCE_TO_TARGET

            if reached_waypoint and self.waypoint_index + 1 < len(self.waypoints):
                self.waypoint_index += 1

        return reached_waypoint

    def reached_any_waypoint(self, drone_point, distance_to_target):
        """
        Return True if the drone mass has reached any waypoint

        :param drone_point: The drone's current position
        :param distance_to_target: Max distance to target
        """
        for waypoint in self:
            reached_waypoint = VectorMath.get_magnitude(drone_point, waypoint) < distance_to_target

            if reached_waypoint:
                return True

        return False

    def __getitem__(self, index):
        return self.waypoints[index]

    def __len__(self):
        return len(self.waypoints)
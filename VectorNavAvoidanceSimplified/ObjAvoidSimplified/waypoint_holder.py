'''
Created on Feb 18, 2017

@author: vtolpegin
'''

class WaypointHolder(object):

    MIN_DISTANCE_TO_TARGET = 5

    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.waypoint_index = 0

    def add_waypoint(self, waypoint):
        self.waypoints.append(waypoint)

    def get_current_waypoint(self):
        return self.waypoints[waypoint_index]

    def reached_current_waypoint(self, drone_mass):
        """
        Return True of the drone mass has has reached the current waypoint

        :param drone_mass: The drone mass to determine distance from
        """
        reached_waypoint = False
        if self.waypoint_index < len(self.waypoints):
            reached_waypoint = drone_mass.get_point().point_within_distance(self.waypoints[self.waypoint_index], MIN_DISTANCE_TO_TARGET)

            if reached_waypoint:
                self.waypoint_index += 1

        return reached_waypoint

    def __len__(self):
        return len(self.waypoints)

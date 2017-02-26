'''
Created on Feb 18, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *

class WaypointHolder(object):

    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.waypoint_index = 0

    def add_waypoint(self, waypoint):
        self.waypoints = np.vstack([self.waypoints, waypoint])

        if self.waypoints.shape()[0] == 2:
            self.waypoints = np.delete(self.waypoints, (0), axis=0)

    def get_current_waypoint(self):
        return self.waypoints[self.waypoint_index]

    def get_velocity_vector_to_next_waypoint(self, drone_current_point, speed):
        unit_vector = VectorMath.get_unit_vector(drone_current_point, self[self.waypoint_index])
        velocity_vector = unit_vector * speed

        self.reached_current_waypoint(drone_current_point)

        return velocity_vector

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

    def draw(self, win):
        for i in range(0, len(self)):
            c = Circle(Point(int(self[i][0] + Window.CENTERPOINT[0]), int(Window.CENTERPOINT[1] - self[i][1])), 3)
            c.setFill("green")
            c.draw(win.getGraphWin())

    def __getitem__(self, index):
        return self.waypoints[index]

    def __len__(self):
        return len(self.waypoints)

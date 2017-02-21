'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *
import numpy as np
import math

class DroneMass(Mass):

    def __init__(self, mass, waypoints):
        super(DroneMass, self).__init__(np.array([0,0]), mass)

        self.velocity_vector = np.zeros(len(self.get_point()))
        self.waypoint_holder = WaypointHolder(waypoints)
        self.speed = Constants.DRONE_SPEED

    def add_waypoint(self, waypoint):
        self.waypoint_holder.add_waypoint(waypoint)

    def apply_motions(self, mass_holder):
        self.set_velocity_vector(self.waypoint_holder.get_velocity_vector_to_next_waypoint(self.get_point(), self.speed))

        net_velocity_vector = self.get_net_velocity_vector(mass_holder)
        self.set_point(self.get_point_after_velocity_applied(self.get_point(), net_velocity_vector))

        return self.determine_direction_change_after_motions()

    def get_point_after_velocity_applied(self, point, velocityVector):
        return point + (velocityVector * Constants.REFRESH_RATE)

    def get_net_velocity_vector(self, mass_holder):
        self.velocity_vector = self.speed * VectorMath.get_unit_vector(self.get_point(), self.waypoint_holder.get_current_waypoint())

        net_force_vector = self.get_net_force_vector(mass_holder)
        new_point = self.get_point() + ((net_force_vector / float(self.mass)) * Constants.REFRESH_RATE**2)
        new_point = self.get_point_after_velocity_applied(new_point, self.velocity_vector)

        new_position_unit_vector = VectorMath.get_unit_vector(self.get_point(), new_point)

        return new_position_unit_vector * self.speed

    def get_waypoint_holder(self):
        return self.waypoint_holder

    def get_current_waypoint(self):
        return self.waypoint_holder.get_current_waypoint()

    def get_net_force_vector(self, mass_holder):
        net_force = np.zeros(len(self.get_point()))
        for mass_index in range(len(mass_holder)):
            force = VectorMath.get_force(self, mass_holder[mass_index], Constants.GRAVITATIONAL_CONSTANT)
            unit_vector = -1.0 * VectorMath.get_unit_vector(self.get_point(), mass_holder[mass_index].get_point())

            net_force += force * unit_vector

        return net_force

    def get_velocity_vector(self):
        return self.velocity_vector

    def set_velocity_vector(self, vector):
        self.velocity_vector = vector

    def determine_direction_change_after_motions(self):
        velocity_unit_vector = VectorMath.get_single_unit_vector(self.get_velocity_vector())
        waypoint_unit_vector = VectorMath.get_unit_vector(self.get_point(), self.get_current_waypoint())
        maximum_difference = math.pi / 60

        diff = np.absolute(np.subtract(velocity_unit_vector, waypoint_unit_vector)) * 10
        if not self.waypoint_holder.reached_any_waypoint(self.get_point(), 50):
            if np.any(np.greater(diff, np.array(maximum_difference))):
                return True

        return False

    def draw(self, win):
        c = Circle(Point(int(self.get_point()[0] + Window.CENTERPOINT[0]), int(Window.CENTERPOINT[1] - self.get_point()[1])), 3)
        c.setFill("red")
        c.draw(win.getGraphWin())

    def __repr__(self):
        returnString = "Drone Mass "
        returnString += Mass.__repr__(self)
        return returnString

from ObjAvoidSimplified import *
import numpy as np
import math

class DroneMass(Mass):

    def __init__(self, mass, waypoints):
        super(DroneMass, self).__init__(np.array([0,0]), mass)

        self.velocity_vector = np.zeros(len(self.get_point()))
        self.waypoint_holder = WaypointHolder(waypoints)
        self.speed = Constants.DRONE_SPEED

        self.color = "red"

        self.guided_distance_threshold = 4

    def add_waypoint(self, waypoint):
        self.waypoint_holder.add_waypoint(waypoint)

    def apply_motions(self, mass_holder):
        self.set_velocity_vector(self.waypoint_holder.get_velocity_vector_to_next_waypoint(self.get_point(), self.speed))

        net_velocity_vector = self.get_net_velocity_vector(mass_holder)
        self.set_point(self.get_point_after_velocity_applied(self.get_point(), net_velocity_vector))

        return self.determine_change_after_motions(mass_holder)

    def get_point_after_velocity_applied(self, point, velocityVector):
        return point + (velocityVector * Constants.REFRESH_RATE)

    def get_net_velocity_vector(self, mass_holder):
        self.velocity_vector = self.speed * VectorMath.get_unit_vector(self.get_point(), self.waypoint_holder.get_current_waypoint())

        net_force_vector = self.get_net_force_vector(mass_holder)
        new_point = self.get_point() + ((net_force_vector / float(self.mass)) * Constants.REFRESH_RATE**2 / 2)
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
            print("net_force: " + str(net_force))

        return net_force

    def get_velocity_vector(self):
        return self.velocity_vector

    def set_velocity_vector(self, vector):
        self.velocity_vector = vector

    def determine_change_after_motions(self, mass_holder):
        for obstacle in mass_holder:
            distance = ((self.get_point()[0] - obstacle.get_point()[0])**2 + (self.get_point()[1] - obstacle.get_point()[1])**2)**0.5
            print("obstacle_dist: " + str(distance))

            if distance / obstacle.get_safety_radius() < self.guided_distance_threshold:
                self.color = "orange"
                return True

        self.color = "red"
        return False

    def __repr__(self):
        returnString = "Drone "
        returnString += Mass.__repr__(self)
        return returnString

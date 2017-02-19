'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *
import numpy as np

class DroneMass(Mass):

    def __init__(self, mass, waypoints):
        super(DroneMass, self).__init__(np.array([0,0]), mass)

        self.force_vector = np.zeros(len(self.get_point()))
        self.waypoint_holder = WaypointHolder(waypoints)
        self.speed = 500

    def add_waypoint(self, waypoint):
        self.waypoint_holder.add_waypoint(waypoint)

    def apply_motions(self, mass_holder):
        # TODO: Apply motions from some masses, return the new coordinates
        return None

    def get_waypoint_holder(self):
        return self.waypoint_holder

    def get_net_force_vector(self, mass_holder):
        # TODO: Get the net force acting on the drone mass
        return None

    def get_velocity_vector(self):
        # TODO: Get the velocity of the drone, with respect
        return None

    def __repr__(self):
        returnString = "Drone Mass "
        returnString += Mass.__repr__(self)
        return returnString

'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *

class DroneMass(Mass):

    DEFAULT_DRONE_MASS = 1

    def __init__(self, bound_mass_holder, mass, waypoints):
        Mass.__init__(self, bound_mass_holder, [0,0], mass)
        self.force_vector = Vector.createEmptyVectorWithDim(len(self.getPoint()))
        self.waypoint_holder = WaypointHolder(waypoints)
        self.speed = 500

    def get_net_force_vector(self, mass_holder):
        # TODO: Get the net force acting on the drone mass

    def apply_motions(self, mass_holder):
        # TODO: Apply motions from some masses, return the new coordinates

    def get_waypoint_holder(self):
        return self.waypoint_holder

    def __repr__(self):
        returnString = "Drone Mass "
        returnString += Mass.__repr__(self)
        return returnString

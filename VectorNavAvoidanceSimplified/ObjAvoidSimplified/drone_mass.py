'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *

class DroneMass(Mass):

    DEFAULT_DRONE_MASS = 1

    def __init__(self, mass, waypoints):
        super(DroneMass, self).__init__([0,0], mass)

        self.force_vector = Vector.createEmptyVectorWithDim(len(self.getPoint()))
        self.waypoint_holder = WaypointHolder(waypoints)
        self.speed = 500

    def get_net_force_vector(self, mass_holder):
        # TODO: Get the net force acting on the drone mass

    def get_velocity_vector(self):
        # TODO: Get the velocity of the drone, with respect

    def apply_motions(self, mass_holder):
        # TODO: Apply motions from some masses, return the new coordinates

    def get_waypoint_holder(self):
        return self.waypoint_holder

    def __repr__(self):
        returnString = "Drone Mass "
        returnString += Mass.__repr__(self)
        return returnString

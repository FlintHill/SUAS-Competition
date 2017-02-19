'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *
import random
import math

class SafetyRadiusMass(Mass):

    def __init__(self, starting_point, mass, safety_radius):
        super(SafetyRadiusMass, self).__init__(starting_point, mass)

        self.safety_radius = safety_radius

    def get_required_mass_to_balance_motion(self, drone_mass):
        # TODO: Do the math to figure out what the mass needs to be
        return self.get_mass()

    def update_mass(self, drone_mass):
        self.set_mass(self.get_required_mass_to_balance_motion(drone_mass))

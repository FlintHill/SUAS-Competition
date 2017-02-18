'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *
import random
import math

class SafetyRadiusMass(Mass):

    def __init__(self, pointIn, massIn, safetyRadiusIn):
        super(SafetyRadiusMass, self).__init__(pointIn, massIn)
        self.safetyRadius = safetyRadiusIn
        self.timeIncrement = timeIncrementIn

    def get_required_mass_to_balance_motion(self, drone_mass):
        gravityUnitVector = self.getVectorToMass(drone_mass).getUnitVector()
        velocityVector = drone_mass.getVelocityVector()
        projVector = gravityUnitVector.getProjectionOntoSelf(velocityVector)
        magProj = projVector.getMagnitude()
        massObject =(2*magProj*self.safetyRadius**2)/(MassHolder.GRAVITY_CONSTANT * self.timeIncrement)
        return massObject

    def update_mass(self, drone_mass):
        self.setMass(self.get_required_mass_to_balance_motion(drone_mass))

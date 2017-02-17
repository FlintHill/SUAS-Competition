'''
Created on Jan 23, 2017

@author: phusisian
'''
from ObjAvoidSimplified import *
import random
import math

class SafetyRadiusMass(Mass):
    def __init__(self, boundMassHolder, pointIn, massIn, safetyRadiusIn, timeIncrementIn):
        super(SafetyRadiusMass, self).__init__(boundMassHolder, pointIn, massIn)
        self.safetyRadius = safetyRadiusIn
        self.timeIncrement = timeIncrementIn

    def get_required_mass_to_balance_motion(self, droneMass):
        gravityUnitVector = self.getVectorToMass(droneMass).getUnitVector()
        velocityVector = droneMass.getVelocityVector()
        projVector = gravityUnitVector.getProjectionOntoSelf(velocityVector)
        magProj = projVector.getMagnitude()
        massObject =(2*magProj*self.safetyRadius**2)/(MassHolder.GRAVITY_CONSTANT * self.timeIncrement)
        return massObject

    def update_mass(self, drone_mass):
        self.setMass(self.get_required_mass_to_balance_motion(drone_mass))

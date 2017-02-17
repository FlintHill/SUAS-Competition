'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplfied import *
import random
import math

class Mass(object):

    def __init__(self, boundMassHolder, pointIn, massIn):
        self.boundMassHolder = boundMassHolder
        self.point = pointIn
        self.mass = massIn

    def getForceVectorToMass(self, massTwo):
        self.updateMass(massTwo)

        magForce = self.getMagnitudeOfForceToMass(massTwo)
        forceUnitVector = self.getVectorToMass(massTwo).getUnitVector()
        return forceUnitVector * magForce

    def getMagnitudeOfForceToMass(self, massTwo):
        return  ((massTwo.getMass() * self.mass)/(self.getVectorToMass(massTwo).getMagnitude())**2) * MassHolder.GRAVITY_CONSTANT

    def getVectorToMass(self, massTwo):
        return self.point.getVectorToPoint(massTwo.getPoint())

    def move2DRandomWithMagnitude(self, magnitude):
        randAngle = random.random()*2*math.pi
        xComp = magnitude * math.cos(randAngle)
        yComp = magnitude * math.sin(randAngle)
        moveVector = Vector([xComp, yComp])
        self.point = self.point + moveVector
        self.drawCircle.move(xComp, -yComp)

    def update_mass(self, massTwo):
        pass

    def get_mass(self):
        return self.mass

    def set_mass(self, massIn):
        self.mass = massIn

    def get_point(self):
        return self.point

    def set_point(self, new_point):
        self.point = new_point

    def __repr__(self):
        returnString = "Mass at: " + str(self.point)
        return returnString

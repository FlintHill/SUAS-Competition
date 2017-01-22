'''
Created on Jan 10, 2017

@author: phusisian
'''
from Vector import Vector
from MassHolder import MassHolder
from graphics import *
from Window import Window
class Mass:
    '''timeStep is the amount of time for which the force is being applied'''
    #DEFAULT_TIMESTEP = .1 #in Ms
    def __init__(self, boundMassHolder, pointIn, massIn):
        self.boundMassHolder = boundMassHolder
        self.point = pointIn
        self.mass = massIn
        #self.velocityVector = Vector([0,0,0])

    def getForceVectorToMass(self, massTwo):
        magForce = self.getMagnitudeOfForceToMass(massTwo)
        forceUnitVector = self.getVectorToMass(massTwo).getUnitVector()
        return forceUnitVector * magForce



    def getMagnitudeOfForceToMass(self, massTwo):
        return  ((massTwo.getMass() * self.mass)/(self.getVectorToMass(massTwo).getMagnitude())**2) * MassHolder.GRAVITY_CONSTANT

    def getVectorToMass(self, massTwo):
        return self.point.getVectorToPoint(massTwo.getPoint())


    def getMass(self):
        return self.mass

    def getPoint(self):
        return self.point

    def draw(self, win):
        c = Circle(Point(int(self.point[0] + win.getCenterPoint()[0]), int(win.getCenterPoint()[1] - self.point[1])), 10)#subtracted so reversed y axis graphics work.
        c.draw(win.getGraphWin())

    def __repr__(self):
        returnString = "Mass at: " + str(self.point)
        return returnString

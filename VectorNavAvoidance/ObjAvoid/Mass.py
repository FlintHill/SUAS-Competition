'''
Created on Jan 10, 2017

@author: phusisian
'''
from ObjAvoid import *
import random
import math

class Mass(object):

    '''timeStep is the amount of time for which the force is being applied'''
    #DEFAULT_TIMESTEP = .1 #in Ms
    def __init__(self, boundMassHolder, pointIn, massIn):
        self.boundMassHolder = boundMassHolder
        self.point = pointIn
        self.mass = massIn
        self.drawCircle = Circle(Point(int(self.point[0] + Window.CENTERPOINT[0]), int(Window.CENTERPOINT[1] - self.point[1])), 5)
        self.drawCircle.setFill("red")
        #self.velocityVector = Vector([0,0,0])

    def getForceVectorToMass(self, massTwo):
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

    def getMass(self):
        return self.mass

    def setMass(self, massIn):
        self.mass = massIn

    def getPoint(self):
        return self.point

    def setPoint(self, newPoint):
        self.point = newPoint

    def draw(self, win):
        #c = Circle(Point(int(self.point[0] + win.getCenterPoint()[0]), int(win.getCenterPoint()[1] - self.point[1])), 5)#subtracted so reversed y axis graphics work.
        #c.setFill("red")
        self.drawCircle.draw(win.getGraphWin())

    def __repr__(self):
        returnString = "Mass at: " + str(self.point)
        return returnString

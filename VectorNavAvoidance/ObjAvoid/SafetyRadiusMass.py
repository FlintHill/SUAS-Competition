'''
Created on Jan 23, 2017

@author: phusisian
'''
from ObjAvoid.Mass import Mass
from ObjAvoid.MassHolder import MassHolder
from ObjAvoid.Window import Window
from ObjAvoid.graphics import *
import random
import math
from ObjAvoid.Vector import Vector

class SafetyRadiusMass(Mass):
    def __init__(self, boundMassHolder, pointIn, massIn, safetyRadiusIn, timeIncrementIn):
        super(SafetyRadiusMass, self).__init__(boundMassHolder, pointIn, massIn)
        self.safetyRadius = safetyRadiusIn
        self.timeIncrement = timeIncrementIn
        self.radiusCircle = Circle(Point(int(self.point[0] + Window.CENTERPOINT[0]), int(Window.CENTERPOINT[1] - self.point[1])), self.safetyRadius)
        self.radiusCircle.setFill("blue")
        
    def move2DRandomWithMagnitude(self, magnitude):
        randAngle = random.random()*2*math.pi
        xComp = magnitude * math.cos(randAngle)
        yComp = magnitude * math.sin(randAngle)
        moveVector = Vector([xComp, yComp])
        self.setPoint(self.point + moveVector)
        self.radiusCircle.move(xComp, -yComp)    
        self.drawCircle.move(xComp, -yComp)
        
    def getRequiredMassToBalanceMotion(self, droneMass):
        gravityUnitVector = self.getVectorToMass(droneMass).getUnitVector()
        #print(gravityUnitVector)
        #print("velocity vector: " + str(droneMass.getVelocityVector()))
        velocityVector = droneMass.getVelocityVector()
        projVector = gravityUnitVector.getProjectionOntoSelf(velocityVector)
        #print(str(projVector))
        magProj = projVector.getMagnitude()
        massObject =(2*magProj*self.safetyRadius**2)/(MassHolder.GRAVITY_CONSTANT * self.timeIncrement)
        return massObject
    
    def updateForce(self, droneMass):
        self.setMass(self.getRequiredMassToBalanceMotion(droneMass))
    
    
    def draw(self, win):
        self.radiusCircle.draw(win.getGraphWin())
        #c = Circle(Point(int(self.point[0] + win.getCenterPoint()[0]), int(win.getCenterPoint()[1] - self.point[1])), self.safetyRadius)#subtracted so reversed y axis graphics work.
        #c.setFill("blue") 
        #c.draw(win.getGraphWin())
        super(SafetyRadiusMass, self).draw(win)
    
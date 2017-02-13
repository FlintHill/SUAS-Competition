'''
Created on Jan 10, 2017

@author: phusisian
'''
from ObjAvoid import *

class DroneMass(Mass):
    DEFAULT_DRONE_MASS = 1

    def __init__(self, boundMassHolder, pointIn, massIn, waypoints):
        Mass.__init__(self, boundMassHolder, pointIn, massIn)
        self.velocityVector = Vector.createEmptyVectorWithDim(len(self.getPoint()))
        self.navVectorMaker = NavVectorMaker(self, waypoints)
        self.speed = 500

    '''currently masses can't have any forces of their own. set netVector to the force of the mass
    if I ever do add it instead of (0,0,0)'''
    def getNetForceVector(self):
        netVector = Vector.createEmptyVectorWithDim(len(self.getPoint()))#Vector([0,0,0])
        for i in range(0, len(self.boundMassHolder)):
            if not self.boundMassHolder[i] == self:
                '''vector casted from that mass to this one, so force should be facing the correct direction.'''
                netVector += self.boundMassHolder[i].getForceVectorToMass(self)
        return netVector

    def applyMotions(self):
        self.navVectorMaker.setVelocityVectorToNextTravelPoint(self.speed)
        self.point = self.getPointAfterVelocityApplied(self.getNetVelocityVector())
        #self.applyForce(self.getNetForceVector())
        #self.applyVelocity(self.getNetVelocityUnitVector(self.getNetForceVector()))
        
    def getPointAfterForceApplied(self, point, forceVector):
        return point + (forceVector * (1.0/float(self.mass))) * (Window.REFRESH_TIME**2) * 0.5
    
    def getPointAfterVelocityApplied(self, point, velocityVector): 
        return point + (velocityVector * Window.REFRESH_TIME)
    
    def getNetVelocityVector(self):
        netForce = self.getNetForceVector()
        newPoint = self.getPointAfterForceApplied(self.point, netForce)
        newPoint = self.getPointAfterVelocityApplied(newPoint, self.getVelocityVector())
        unitNetVelocityVector = self.point.getUnitVectorToPoint(newPoint)
        return unitNetVelocityVector * self.speed
    
    '''
    def getNetVelocityUnitVector(self, forceVector):
        newPoint = self.getVelocityDirectionPoint(forceVector)
        return self.point.getUnitVectorToPoint(newPoint)
        
    def getVelocityDirectionPoint(self, forceVector):
        newPoint = self.getPositionAfterForce(self.point.clone(), forceVector)
        newPoint += self.velocityVector * Window.REFRESH_TIME
        return newPoint
    
    def getPositionAfterForce(self, point, forceVector):
        return point + (forceVector*(1.0/float(self.mass)))*(Window.REFRESH_TIME**2)*0.5
    '''
    '''
    def applyForce(self, force):
        #(1/2) at^2
        self.point += (force*(1.0/float(self.mass)))*(Window.REFRESH_TIME**2)*0.5
    '''
    '''
    def getPushVelocityVector(self, forceVector):
        pushVelocity = (forceVector*(1.0/float(self.mass))*Window.REFRESH_TIME)*0.5
        return pushVelocity
    '''
    '''
    def getNetVelocityUnitVector(self, forceVector):
        return (self.velocityVector + self.getPushVelocityVector(forceVector)).getUnitVector()
    '''
    def applyVelocity(self, forceVector):
        self.point += self.getNetVelocityUnitVector(forceVector) * self.speed * Window.REFRESH_TIME
        print("velocity applied. New point: " + str(self.point))

    def draw(self, win):
        self.point.draw(win, "red")

    def getNavVectorMaker(self):
        return self.navVectorMaker

    def setSpeed(self, speedIn):
        self.speed = speedIn

    def getSpeed(self):
        return self.speed

    def setVelocityVector(self, vectorIn):
        self.velocityVector = vectorIn

    def getVelocityVector(self):
        return self.velocityVector

    def __repr__(self):
        returnString = "Drone Mass "
        returnString += Mass.__repr__(self)
        return returnString

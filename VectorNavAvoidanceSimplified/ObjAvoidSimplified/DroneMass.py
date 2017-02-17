'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *

class DroneMass(Mass):

    DEFAULT_DRONE_MASS = 1

    def __init__(self, bound_mass_holder, mass, waypoints, starting_point=[0,0]):
        Mass.__init__(self, bound_mass_holder, starting_point, mass)
        self.force_vector = Vector.createEmptyVectorWithDim(len(self.getPoint()))
        self.waypoint_holder = WaypointHolder(waypoints)
        self.speed = 500

    def get_net_force(self, masses):
        net_vector = Vector.createEmptyVectorWithDim(len(self.get_point()))
        for index in range(len(masses)):


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
        self.point = self.getPointAfterVelocityApplied(self.getPoint(), self.getNetVelocityVector())

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

    def applyVelocity(self, forceVector):
        self.point += self.getNetVelocityUnitVector(forceVector) * self.speed * Window.REFRESH_TIME
        print("velocity applied. New point: " + str(self.point))

    def get_waypoint_holder(self):
        return self.waypoint_holder

    def setVelocityVector(self, vectorIn):
        self.velocityVector = vectorIn

    def getVelocityVector(self):
        return self.velocityVector

    def __repr__(self):
        returnString = "Drone Mass "
        returnString += Mass.__repr__(self)
        return returnString

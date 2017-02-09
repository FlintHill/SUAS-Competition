'''
Created on Jan 23, 2017

@author: phusisian
'''
class NavVectorMaker:
    
    MIN_DISTANCE_TO_TARGET = 10
    
    def __init__(self, droneMassIn, travelPointsIn):
        self.droneMass = droneMassIn
        self.travelPoints = travelPointsIn
        self.travelIndex = 0
        
    def add_waypoint(self, waypointIn):
        self.travelPoints.append(waypointIn)    
    
    def setVelocityVectorToNextTravelPoint(self, speed):
        unitVector = self.droneMass.getPoint().getUnitVectorToPoint(self.travelPoints[self.travelIndex])
        velocityVector = unitVector * speed
        self.droneMass.setVelocityVector(velocityVector)
        if self.droneMass.getPoint().pointWithinDistance(self.travelPoints[self.travelIndex], NavVectorMaker.MIN_DISTANCE_TO_TARGET) and self.travelIndex < len(self.travelPoints) - 1:
            self.travelIndex += 1
            
    def draw(self, win):
        for i in range(0, len(self.travelPoints)):
            self.travelPoints[i].draw(win, "green")
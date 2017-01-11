'''
Created on Jan 10, 2017

@author: phusisian
'''
from ObjAvoid.MultiDimPoint import MultiDimPoint

class MassHolder:
    GRAVITY_CONSTANT = 5000
    def __init__(self):
        self.masses = []
        self.droneMasses = []
        
    def __getitem__(self, index):
        return self.masses[index]
    
    def __len__(self):
        return len(self.masses)
    
    def appendMass(self, massIn):
        self.masses.append(massIn)
    
    def appendDroneMass(self, droneMassIn):
        self.droneMasses.append(droneMassIn)
    
    def tick(self):
        for i in range(0, len(self.droneMasses)):
            self.droneMasses[i].applyMotions()
            
    def draw(self, win):
        for i in range(0, len(self)):
            self[i].draw(win)
        
        middlePoint = MultiDimPoint([700,-500])
        for i in range(0, len(self.droneMasses)):
            midVector = self.droneMasses[i].getPoint().getVectorToPoint(middlePoint).getUnitVector()
            self.droneMasses[i].setVelocityVector(midVector * 100)
            self.droneMasses[i].draw(win)
            
    def __repr__(self):
        outString = ""
        for i in range(0, len(self)):
            outString += str(self[i]) + "\n"
        for i in range(0, len(self.droneMasses)):
            outString += str(self.droneMasses[i]) + "\n"
        return outString
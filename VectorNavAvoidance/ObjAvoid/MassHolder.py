'''
Created on Jan 10, 2017

@author: phusisian
'''
from ObjAvoid import MultiDimPoint

class MassHolder:

    GRAVITY_CONSTANT = 5000

    def __init__(self):
        self.masses = []
        self.droneMasses = []
        self.tickCount = 0

    def __getitem__(self, index):
        return self.masses[index]

    def __len__(self):
        return len(self.masses)

    def appendMass(self, massIn):
        self.masses.append(massIn)

    def appendDroneMass(self, droneMassIn):
        self.droneMasses.append(droneMassIn)

    def tick(self):
        for index in range(0, len(self.droneMasses)):
            self.droneMasses[index].applyMotions()
    
    def drawStationaryObjects(self, win):
        for i in range(0, len(self)):
            self[i].draw(win)
        for i in range(0, len(self.droneMasses)):
            self.droneMasses[i].getNavVectorMaker().draw(win)

    def draw(self, win):
        '''for i in range(0, len(self)):
            self[i].draw(win)'''

        #middlePoint = MultiDimPoint([700,-500])
        '''for i in range(0, len(self)):
            self[i].draw(win)'''
        for i in range(0, len(self.droneMasses)):
            self.droneMasses[i].draw(win)

    def __repr__(self):
        outString = ""
        for i in range(0, len(self)):
            outString += str(self[i]) + "\n"
        for i in range(0, len(self.droneMasses)):
            outString += str(self.droneMasses[i]) + "\n"
        return outString

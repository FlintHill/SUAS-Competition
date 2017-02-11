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

    def getDroneForceVectors(self):
        droneForceVectors = []
        for i in range(0, len(self.droneMasses)):
            droneForceVectors.append(self.droneMasses[i].getNetForceVector())

        return droneForceVectors

    def tick(self):
        for i in range(0, len(self.droneMasses)):
            for j in range(0, len(self)):
                self[j].updateForce(self.droneMasses[i])
            self.droneMasses[i].applyMotions()

        if self.tickCount > 20:
            self.tickMasses()
            self.tickCount = 0
        self.tickCount += 1

    def tickMasses(self):
        for i in range(0, len(self)):
            self[i].move2DRandomWithMagnitude(40)

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

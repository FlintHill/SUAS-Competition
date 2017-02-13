'''
Created on Jan 10, 2017

@author: phusisian
'''
import random
from ObjAvoid import *

class Test:

    def __init__(self):
        self.massHolder = MassHolder()
        self.droneMass = DroneMass(self.massHolder, MultiDimPoint([0,0]), 1, [])
        self.massHolder.appendDroneMass(self.droneMass)
        self.addRandomMasses(10)
        self.window = Window(self.massHolder, (1440,900))

    def addRandomMasses(self, numMasses):
        #randomPointMaker = RandomPointMaker(2, ((-700, 700), (-500, 500)))
        '''for i in range(0, numMasses):
            randPoint = randomPointMaker.createRandomPoint()
            mass = SafetyRadiusMass(self.massHolder, randPoint, 500, 10, Window.REFRESH_TIME)
            self.massHolder.appendMass(mass)'''
        randPoints = TestFunctions.getRandomPointsInBounds(2, numMasses, ((-700, 700), (-500, 500)))
        for i in range(0, len(randPoints)):
            self.massHolder.appendMass(SafetyRadiusMass(self.massHolder, randPoints[i], 500, 20, Window.REFRESH_TIME))

    def drawStationaryObjects(self, win):
        self.massHolder.drawStationaryObjects(win)

    def draw(self, win):
        self.massHolder.tick()
        self.massHolder.draw(win)

if __name__ == '__main__':
    my_test = Test()

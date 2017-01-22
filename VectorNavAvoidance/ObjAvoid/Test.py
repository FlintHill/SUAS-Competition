'''
Created on Jan 10, 2017

@author: phusisian
'''
from MultiDimPoint import MultiDimPoint
from Vector import Vector
from Mass import Mass
from MassHolder import MassHolder
from DroneMass import DroneMass
from time import sleep
from RandomPointMaker import RandomPointMaker
class Test:
    def __init__(self):
        self.massHolder = MassHolder()
        self.droneMass = DroneMass(self.massHolder, MultiDimPoint([0,0]), 1)
        '''is creating 2d points for sake of being able to easily draw them on the screen.'''
        self.massHolder.appendDroneMass(self.droneMass)
        self.addRandomMasses(150)

    def addRandomMasses(self, numMasses):
        randomPointMaker = RandomPointMaker(2, ((-700, 700), (-500, 500)))
        for i in range(0, numMasses):
            randPoint = randomPointMaker.createRandomPoint()
            mass = Mass(self.massHolder, randPoint, 500)
            self.massHolder.appendMass(mass)

    def draw(self, win):
        self.massHolder.tick()
        self.massHolder.draw(win)

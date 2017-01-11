'''
Created on Jan 10, 2017

@author: phusisian
'''
from ObjAvoid.MultiDimPoint import MultiDimPoint
from ObjAvoid.Vector import Vector
from ObjAvoid.Mass import Mass
from ObjAvoid.MassHolder import MassHolder
from ObjAvoid.DroneMass import DroneMass
from time import sleep
from ObjAvoid.RandomPointMaker import RandomPointMaker
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
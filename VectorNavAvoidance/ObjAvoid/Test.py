'''
Created on Jan 10, 2017

@author: phusisian
'''
from ObjAvoid.MultiDimPoint import MultiDimPoint
import random
from ObjAvoid.Vector import Vector
from ObjAvoid.Mass import Mass
from ObjAvoid.MassHolder import MassHolder
from ObjAvoid.DroneMass import DroneMass
from time import sleep
from ObjAvoid.SafetyRadiusMass import SafetyRadiusMass
from ObjAvoid.RandomPointMaker import RandomPointMaker
from ObjAvoid.Window import Window
from ObjAvoid.TestFunctions import TestFunctions
class Test:
    def __init__(self):
        self.massHolder = MassHolder()
        self.droneMass = DroneMass(self.massHolder, MultiDimPoint([0,0]), 1)
        '''is creating 2d points for sake of being able to easily draw them on the screen.'''
        self.massHolder.appendDroneMass(self.droneMass)
        self.addRandomMasses(50)
    
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
        
    
#class TestFunctions:
    
    
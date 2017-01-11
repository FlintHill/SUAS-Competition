'''
Created on Jan 10, 2017

@author: phusisian
'''
from ObjAvoid.MultiDimPoint import MultiDimPoint
from random import randint
class RandomPointMaker:
    def __init__(self, numDimensions, bounds):
        self.numDimensions = numDimensions
        self.bounds = bounds
    
    def createRandomPoint(self):
        components = []
        for i in range(0, self.numDimensions):
            components.append(self.getRandomComponentInBounds(self.bounds[i]))
        return MultiDimPoint(components)
            
    def getRandomComponentInBounds(self, componentSizeBounds):
        return randint(componentSizeBounds[0], componentSizeBounds[1]-1)
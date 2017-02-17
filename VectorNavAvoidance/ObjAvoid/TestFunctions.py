'''
Created on Jan 24, 2017

@author: phusisian
'''

import random
from ObjAvoid import MultiDimPoint

class TestFunctions:

    @staticmethod
    def getRandomPointsInBounds(dimensions, numPoints, bounds):
        points = []
        for i in range(0, numPoints):
            components = []
            for dim in range(0, dimensions):
                randComp = random.randint(bounds[dim][0], bounds[dim][1])
                components.append(randComp)
            points.append(MultiDimPoint(components))
        return points

    @staticmethod
    def getRandomPointsInBoundsDrone(dimensions, numPoints, specified_altitude, bounds):
        points = []
        for i in range(0, numPoints):
            components = []
            for dim in range(0, dimensions):
                randComp = random.randint(bounds[dim][0], bounds[dim][1])
                components.append(randComp)
            components.append(specified_altitude)
            points.append(MultiDimPoint(components))
        return points

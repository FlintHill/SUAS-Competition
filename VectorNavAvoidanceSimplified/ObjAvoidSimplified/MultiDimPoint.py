'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from math import sqrt
from ObjAvoidSimplified import *

class MultiDimPoint:

    BASE_RADIUS = 3

    def __init__(self, coords):
        self.coords = coords

    def get_vector_to_point(self, secondPoint):
        components = []
        try:
            for i in range(0, len(self)):
                components.append(secondPoint[i]-self[i])
            return Vector(components)
        except:
            raise ValueError("Points have different dimensions")

    def getUnitVectorToPoint(self, secondPoint):
        vector = self.getVectorToPoint(secondPoint)
        return vector.getUnitVector()

    def point_within_distance(self, pointTwo, distance):
        mag = self.getVectorToPoint(pointTwo).getMagnitude()
        return (mag < distance)

    def clone(self):
        return MultiDimPoint(self.coords)

    def __getitem__(self, index):
        return self.coords[index]

    def __len__(self):
        return len(self.coords)

    def __iadd__(self, vectorIn):
        try:
            for i in range(0, len(vectorIn)):
                self.coords[i] += vectorIn[i]
            return self
        except:
            raise ValueError("Vector and point do not have same dimensions")
            return None

    def __add__(self, vectorIn):
        newCoords = []
        try:
            for i in range(0, len(vectorIn)):
                newCoords.append(self.coords[i] + vectorIn[i])
            return MultiDimPoint(newCoords)
        except:
            raise ValueError("Vector and point do not ahve same dimensions")
            return None

    def __repr__(self):
        strOut = ""
        for i in range(0, len(self)):
            strOut += ", " + str(self[i])
        return strOut

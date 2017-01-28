'''
Created on Jan 10, 2017

@author: phusisian
'''
from math import sqrt
from Vector import Vector
from graphics import *
from ThreeDDraw import ThreeDDraw
from Window import Window

class MultiDimPoint:
    BASE_RADIUS = 3
    def __init__(self, coords):
        self.coords = coords

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

    def getVectorToPoint(self, secondPoint):
        components = []
        try:
            for i in range(0, len(self)):
                components.append(secondPoint[i]-self[i])
            return Vector(components)
        except:
            raise ValueError("Points have different dimensions")
            return None

    def getUnitVectorToPoint(self, secondPoint):
        vector = self.getVectorToPoint(secondPoint)
        return vector.getUnitVector()

    def pointWithinDistance(self, pointTwo, distance):
        mag = self.getVectorToPoint(pointTwo).getMagnitude()
        return (mag < distance)

    def draw(self, win, color):
        if len(self) == 3:
            c = Circle(Point(int(self[0] + Window.CENTERPOINT[0]), int(Window.CENTERPOINT[1] - self[1])), ThreeDDraw.getScaledNumber(self[2], MultiDimPoint.BASE_RADIUS))#subtracted so reversed y axis graphics work.
            c.setFill(color)
            c.draw(win.getGraphWin())
        else:
            c = Circle(Point(int(self[0] + Window.CENTERPOINT[0]), int(Window.CENTERPOINT[1] - self[1])), MultiDimPoint.BASE_RADIUS)#subtracted so reversed y axis graphics work.
            c.setFill(color)
            c.draw(win.getGraphWin())

    def __repr__(self):
        strOut = ""
        for i in range(0, len(self)):
            strOut += ", " + str(self[i])
        return strOut

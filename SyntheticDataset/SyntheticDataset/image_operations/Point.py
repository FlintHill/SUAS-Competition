import math

class Point(object):
    '''container class for a point. Stores values and handles simple cartesian math'''

    def __init__(self, xIn, yIn):
        self.x = xIn
        self.y = yIn

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, xIn):
        self.x=xIn

    def setY(self, yIn):
        self.y=yIn

    def __getitem__(self, index):
        if index == 0:
            return self.x
        else:
            return self.y

    '''returns a point with x value of delta x, y value of delta y that would move this point to the compare point'''
    def getTranslatePoint(self, comparePoint):
        return Point(comparePoint.getX() - self.x, comparePoint.getY() - self.y)

    '''returns a point that is this point move by translate point's x, and translate point's y'''
    def getTranslatedPoint(self, translatePoint):
        return Point(self.x + translatePoint.getX(), self.y + translatePoint.getY())

    '''returns the point with x and y coordinates as ints'''
    def toInt(self):
        return Point(int(self.x), int(self.y))

    '''rotates this point around the "pivot" with an angle amount, in radians, "spin"'''
    def rotate(self, pivot, spin):#may have issues with the origin being at the top left corner
        dy = self.y-pivot.getY()
        dx = self.x-pivot.getX()
        radius = math.sqrt(dy**2 + dx**2)
        initTheta = math.atan2(dy, dx)
        self.x = pivot.getX() + radius*math.cos(initTheta+spin)
        self.y = pivot.getY() + radius*math.sin(initTheta+spin)

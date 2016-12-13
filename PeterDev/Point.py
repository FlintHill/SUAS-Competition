import math

class Point:
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

    def rotate(self, pivot, spin):#may have issues with the origin being at the top left corner
        dy = self.y-pivot.getY()
        dx = self.x-pivot.getX()
        radius = math.sqrt(dy**2 + dx**2) 
        initTheta = math.atan2(dy, dx)
        self.x = radius*math.cos(initTheta+spin)
        self.y = radius*math.sin(initTheta+spin)
    
        
        
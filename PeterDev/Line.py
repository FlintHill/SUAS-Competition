'''
Created on Nov 8, 2016

@author: phusisian
'''
from PIL import ImageDraw

class Line:
    
    def __init__(self, p1In, p2In):
        self.p1 = p1In
        self.p2 = p2In
    
    def getSlope(self):
        if self.p2.getX() - self.p1.getX() != 0:
            return float(self.p2.getY() - self.p1.getY())/float(self.p2.getX() - self.p1.getX())
        else:
            return 100000
    
    def getdy(self):
        return self.p2.getY() - self.p1.getY()

    def getdx(self):
        return self.p2.getX() - self.p1.getX()
    
    def drawLine(self, imgIn, color):
        #image = imgIn.load()
        draw = ImageDraw.Draw(imgIn)
        draw.line((self.p1.getX(), self.p1.getY(), self.p2.getX(), self.p2.getY()), color)
        return imgIn
    
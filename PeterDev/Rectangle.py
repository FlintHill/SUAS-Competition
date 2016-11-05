'''
Created on Nov 3, 2016

@author: phusisian
'''

class Rectangle:
    def __init__(self, xIn, yIn, widthIn, heightIn):
        self.x = xIn
        self.y = yIn
        self.width = widthIn
        self.height = heightIn
        
    def getHeight(self):
        return self.height
    def getWidth(self):
        return self.width
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self, xIn):
        self.x = xIn
    def setY(self, yIn):
        self.y = yIn
    def setWidth(self, widthIn):
        self.width = widthIn
    def setHeight(self, heightIn):
        self.height = heightIn
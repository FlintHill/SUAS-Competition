'''
Created on Nov 3, 2016

@author: phusisian
'''
'''
Created on Oct 20, 2016

@author: phusisian
'''

from PIL import Image
import time
import os.path
import math
import numpy
from matplotlib.pyplot import colors
from SystemEvents.Standard_Suite import color
from Carbon.Aliases import true
import sys
import EdgeDetection

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
    def rotate(self, pivot, spin):#may have issues with the origin being at the top left corner
        dy = self.y-pivot.getY()
        dx = self.x-pivot.getX()
        radius = math.sqrt(dy**2 + dx**2) 
        initTheta = math.atan2(dy, dx)
        self.x = radius*math.cos(initTheta+spin)
        self.y = radius*math.sin(initTheta+spin)
    
        
        
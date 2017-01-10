'''
Created on Dec 2, 2016

@author: phusisian
'''

from root.nested.Point import Point
from PIL import Image
import math

class CannyEdge:
    @staticmethod
    def getCannyEdgeImage(sobelEdge, upperThreshold, lowerThreshold):
        img = Image.new("RGB", (len(sobelEdge.getGradientsX()), len(sobelEdge.getGradientsX()[0])))
        image = img.load()
        dim = img.size
        
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if CannyEdge.isMaximumAcrossAngle(sobelEdge, x, y) and sobelEdge.getSobelEdgeImage()[x,y][0] > upperThreshold:
                    image[x,y] = (255,255,255)
        
        
        #***currently no historeisis thresholding***
        
        return img 
         
         
    #def getThresholdPoints(self, sobelEdge, cannyImg, cannyImage, upperThreshold, lowerThreshold):
        
    #Experiment with using check pixels not directly next to pixel (maybe rcos(angle), rsin(angle) where r = 2 or more)
    @staticmethod
    def isMaximumAcrossAngle(sobelEdge, x, y):
        dim = sobelEdge.getSobelEdgeImg().size
        if x > 0 and x < dim[0] - 1 and y > 0 and y < dim[1] - 1:
            perpAngle = sobelEdge.getAngles()[x][y] + (math.pi/4.0)
            sideColorOneNum = sobelEdge.getSobelEdgeImage()[int(x + round(math.cos(perpAngle))), int(y + round(math.sin(perpAngle)))][0]
            sideColorTwoNum = sobelEdge.getSobelEdgeImage()[int(x - round(math.cos(perpAngle))), int(y - round(math.sin(perpAngle)))][0]
            pixelColorNum = sobelEdge.getSobelEdgeImage()[x,y][0]
            
            if pixelColorNum >= sideColorOneNum and pixelColorNum >= sideColorTwoNum:
                return True
            
        return False
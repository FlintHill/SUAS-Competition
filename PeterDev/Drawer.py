'''
Created on Dec 6, 2016

@author: phusisian
'''
import math
class Drawer:
    
    @staticmethod
    def drawDotOnPixel(image, x, y, color):
        image[x,y] = color
        
    @staticmethod
    def fillRect(img, image, rect, color):
        for x in range(rect.getX(), rect.getX() + rect.getWidth()):
            for y in range(rect.getY(), rect.getY() + rect.getHeight()):
                if x < img.size[0] and x >= 0 and y < img.size[1] and y >= 0:
                    image[x,y] = color
                    
    @staticmethod
    def drawCircle(img, image, point, radius, color, numSteps = 64):
        theta = 0
        thetaInc = 2*math.pi/float(numSteps)
        while theta < math.pi*2.0:
            try:
                x = point[0] + int(radius * math.cos(theta))
                y = point[1] + int(radius * math.sin(theta))
                image[x,y] = color
            except: 
                pass
            theta += thetaInc
        
        
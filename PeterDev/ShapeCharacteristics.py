'''
Created on Nov 4, 2016

@author: phusisian
'''
import Point
import math

class ShapeCharacteristics:
    def countSides(self, imgIn, boundingRect):##PROBLEM: setting radius to exactly 1/2 of the lowest dimension can lead the point to just barely clip out of the shape and not be counted as in or out. The margin to subtract from the radius is arbitrarily set(as of now it is set to subtract 5% of the shorter side's pixel width/height).
        image = imgIn.load()
        radius= 0
        numIncrements = 48
        centerPoint = Point.Point(boundingRect.getX() + (boundingRect.getWidth()/2.0), boundingRect.getY() + (boundingRect.getHeight()/2.0))
        if boundingRect.getWidth() < boundingRect.getHeight():
            radius = float(boundingRect.getWidth()/2.0) - 0.05*boundingRect.getWidth()
        else:
            radius = float(boundingRect.getHeight()/2.0) - 0.05*boundingRect.getHeight()
        
        
        numSwitched = 0
        dAngle = float(2*math.pi/numIncrements)
        prevColor = image[int(boundingRect.getX() + boundingRect.getWidth()), int(centerPoint.getY())]
        for i in range(1, numIncrements + 1):
            x = centerPoint.getX() + radius*math.cos(i*dAngle)
            y = centerPoint.getY() + radius*math.sin(i*dAngle)
            
            if image[x,y] != prevColor:
                numSwitched += 1
            prevColor = image[x,y]
            image[x,y] = (255,255,255)
        return numSwitched/2
    
    def countSidesWithLayer(self, layers, boundingRect):
        
        radius= 0
        numIncrements = 48
        centerPoint = Point.Point(boundingRect.getX() + (boundingRect.getWidth()/2.0), boundingRect.getY() + (boundingRect.getHeight()/2.0))
        if boundingRect.getWidth() < boundingRect.getHeight():
            radius = float(boundingRect.getWidth()/2.0) - 0.05*boundingRect.getWidth()
        else:
            radius = float(boundingRect.getHeight()/2.0) - 0.05*boundingRect.getHeight()
        
        
        numSwitched = 0
        dAngle = float(2*math.pi/numIncrements)
        prevLayer = layers[int(boundingRect.getX() + boundingRect.getWidth())][int(centerPoint.getY())]
        for i in range(1, numIncrements + 1):
            x = int(centerPoint.getX() + radius*math.cos(i*dAngle))
            y = int(centerPoint.getY() + radius*math.sin(i*dAngle))
            
            if layers[x][y] != prevLayer:
                numSwitched += 1
            prevLayer = layers[x][y]
            
        return numSwitched/2
        #for x in range(boundingRect.getX(), boundingRect.getX() + boundingRect.getWidth()):
            
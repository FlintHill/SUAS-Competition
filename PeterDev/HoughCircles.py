'''
Created on Jan 8, 2017

@author: phusisian
'''
import math
from root.nested.Drawer import Drawer
from root.nested.Point import Point
from root.nested.Circle import Circle
class HoughCircles:
    BLOB_SIZE = 3
    RADIUS_STEP = 1
    THETA_STEP = math.pi/64.0#replace theta_step with 1/circumference of circle so it hits each point once only, and doesn't skip any
    '''needs imprecision adjustments -- lossy rounding, things falling in the wrong block, etc. will allow me to speed it up by
    making it less over-precise'''
    '''takes the canny img and image'''
    def __init__(self, img, image, radiusBounds):
        self.img = img
        self.image = image
        self.radiusBounds = radiusBounds
        self.initAccumulatorMatrix()
        
    def initAccumulatorMatrix(self):
        self.accumulatorMatrix = [[HoughPoint((x,y), self.radiusBounds) for y in range(0, self.img.size[1])] for x in range(0, self.img.size[0])]
        
        radius = self.radiusBounds[0]
        while radius < self.radiusBounds[1]:
            theta = 0
            
            theta_step = 2.0*math.pi/(2.0*math.pi*radius)
            while theta < math.pi*2.0:
                sinTheta = math.sin(theta)
                cosTheta = math.cos(theta)
                rSinTheta = int(sinTheta * radius)
                rCosTheta = int(cosTheta * radius)
                #radius = self.radiusBounds[0]
                for x in range(0, self.img.size[0]):
                    for y in range(0, self.img.size[1]):
                        if self.image[x,y] != (0,0,0) and self.image[x,y] != (0,0,0,0):
                            #print("current pixel: " + str((x,y)))
                            
                            xPoint = x+rCosTheta
                            yPoint = y-rSinTheta
                            
                            if xPoint > 0 and xPoint < self.img.size[0] and yPoint > 0 and yPoint < self.img.size[1]:
                                
                                self.accumulatorMatrix[xPoint][yPoint].addVoteAtRadius(radius)
                                
                theta += theta_step
                                
                
            radius += HoughCircles.RADIUS_STEP
        
    '''    
    def getHighestVoteWeightPoint(self):
        highestVote = self.accumulatorMatrix[0][0].getGreatestVoteWeight()
        highestIndexes = (0,0)
        for x in range(0, len(self.accumulatorMatrix)):
            for y in range(0, len(self.accumulatorMatrix[0])):
                iterVote = self.accumulatorMatrix[x][y].getGreatestVoteWeight()
                if iterVote > highestVote:
                    highestVote = iterVote
                    highestIndexes = (x,y)
                    
        return highestIndexes'''
    
    def circleCirclesOverThreshold(self, img, image, threshold):
        circles = self.getCirclesOverThreshold(threshold)
        for circle in circles:
            Drawer.drawCircle(img, image, Point(circle[0], circle[1]), circle.getRadius(), (255,0,0))
        return img
        '''for x in range(0, len(self.accumulatorMatrix)):
            for y in range(0, len(self.accumulatorMatrix[0])):
                pixelRadiusVote = self.accumulatorMatrix[x][y].getGreatestVote()
                if pixelRadiusVote.getVote() > threshold:
                    Drawer.drawCircle(img, image, Point(x,y), pixelRadiusVote.getRadius(), (255,0,0))
        return img'''
    
    def getCirclesOverThreshold(self, threshold):
        circles = []
        for x in range(0, len(self.accumulatorMatrix)):
            for y in range(0, len(self.accumulatorMatrix[0])):
                pixelRadiusVote = self.accumulatorMatrix[x][y].getGreatestVote()
                if pixelRadiusVote.getVote() > threshold:
                    circles.append(Circle((x,y), pixelRadiusVote.getRadius()))
        return circles
            
    def getHighestRadiusVotePoint(self):
        highestVote = self.accumulatorMatrix[0][0].getGreatestVoteWeight()
        highestIndexes = (0,0)
        for x in range(0, len(self.accumulatorMatrix)):
            for y in range(0, len(self.accumulatorMatrix[0])):
                iterVote = self.accumulatorMatrix[x][y].getGreatestVote()
                if iterVote.getVote() > highestVote.getVote():
                    highestVote = iterVote
                    highestIndexes = (x,y)
        
        return (highestIndexes[0], highestIndexes[1], highestVote.getRadius())
        
class HoughPoint:
    def __init__(self, position, radiusBounds):
        self.pos = position
        self.radiusBounds = radiusBounds
        self.initVoteArray()
        
    def initVoteArray(self):
        self.votes = [RadiusVote(i) for i in range(self.radiusBounds[0], self.radiusBounds[1], HoughCircles.RADIUS_STEP)]
        #print ("votes: " + str(self.votes))
    
    def addVoteAtRadius(self, radius):
        for i in range(0, len(self.votes)):
            if self.votes[i].getRadius() == radius:
                self.votes[i].addVote()
        
    '''def getIndexOfRadius(self, radius):
        #
        return int((radius - self.radiusBounds[0])/HoughCircles.RADIUS_STEP)
    '''
    def getGreatestVote(self):
        greatestIndex = 0
        for i in range(1, len(self.votes)):
            if self.votes[i].getVote() > self.votes[greatestIndex].getVote():
                greatestIndex = i
        return self.votes[greatestIndex]

class RadiusVote:
    
    def __init__(self, radius):
        self.radius = radius
        self.vote = 0
        
    def addVote(self):
        self.vote += 1
    
    '''def __iadd__(self, amount):
        self.vote += amount
    '''
    
    
    def getRadius(self):
        return self.radius
    
    '''def __getitem__(self):
        return self.vote'''
    
    def getVote(self):
        return self.vote
        
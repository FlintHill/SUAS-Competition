'''
Created on Feb 4, 2017

@author: phusisian
'''

from math import sin, cos, sqrt, pi
from PIL import Image
class SWT:
    LOWER_VECTOR_THRESHOLD = 5
    def __init__(self, sobelEdgeIn, cannyImgIn, cannyImageIn):
        self.sobelEdge = sobelEdgeIn
        self.cannyImg = cannyImgIn
        self.cannyImage = cannyImageIn
        self.initSWTVectors()
        
    def initSWTVectors(self):
        self.SWTVectors = []
        for x in range(0, self.cannyImg.size[0]):
            for y in range(0, self.cannyImg.size[1]):
                if(self.cannyImage[x,y] != (0,0,0)):
                    addTheta = -pi/4.0
                    #print(self.sobelEdge.getAngles()[x][y])
                    dx = cos(self.sobelEdge.getAngles()[x][y] + addTheta)
                    dy = -sin(self.sobelEdge.getAngles()[x][y] + addTheta)
                    dxSum = x#x + dx
                    dySum = y#y + dy
                    #pixel = (int(round(dxSum)), int(round(dySum)))
                    
                    #print("X: " + str(x))
                    #print("Y: " + str(y))
                    stopIter = False
                    while(not stopIter):
                        dxSum += dx
                        dySum += dy
                        if self.pixelIsInBounds((int(dxSum), int(dySum))):
                            #print("dxsum: " + str(dxSum) + ", dysum: " + str(dySum))
                            if self.pixelIsEdge((int(dxSum), int(dySum))) and (int(dxSum) != x and int(dySum) != y):
                                addVector = SWTVector((x,y), (dxSum, dySum))
                                self.SWTVectors.append(addVector)
                                stopIter = True
                        else:
                            stopIter = True
                            '''
                    #while(self.pixelIsInBounds((int(dxSum), int(dySum))) and not self.pixelIsEdge((int(dxSum), int(dySum)))):# or (int(dxSum) == x and int(dySum) == y)):
                        #dxSum += dx
                        #dySum += dy
                        #print("dxsum: " + str(dxSum) + ", dysum: " + str(dySum))
                        #pixel = (int(round(dxSum)), int(round(dySum)))
                    
                    #pixel = (int(round(dxSum)), int(round(dySum)))
                    if(not self.pixelIsInBounds((int(dxSum), int(dySum)))):
                        addVector = SWTVector((x,y), (dxSum, dySum))
                        self.SWTVectors.append(addVector)'''
                        
        print(self.SWTVectors)
        self.removeSmallVectors()
        self.setVectorsAboveMeanToMean()
    
    def removeSmallVectors(self):
        i = 0
        print("removing small vectors")
        while i < len(self.SWTVectors):
            if self.SWTVectors[i].getMagnitude() <= SWT.LOWER_VECTOR_THRESHOLD:
                del self.SWTVectors[i]
            else:
                i+=1

    def getMean(self):
        sum = 0
        i = 0
        while i < len(self.SWTVectors):
            sum += self.SWTVectors[i].getMagnitude()
            i += 1
        return float(sum)/float(len(self.SWTVectors))
    
    def setVectorsAboveMeanToMean(self):
        mean = self.getMean()
        print("setting above mean to mean")
        for i in range(0, len(self.SWTVectors)):
            if self.SWTVectors[i] > mean:
                self.SWTVectors[i].setMagnitudeAboutMidpoint(mean)
    
    def getFrameImg(self, color):
        img = Image.new("RGB", self.cannyImg.size, (0,0,0))
        image = img.load()
        for i in range(0, len(self.SWTVectors)):
            print("i: " + str(i) +", len: " + str(len(self.SWTVectors)))
            self.SWTVectors[i].drawMidpointOntoImage(image, color)
        return img
        
    
    def pixelIsInBounds(self, pixel):
        return((pixel[0] < self.cannyImg.size[0] and pixel[0] > 0 and pixel[1] < self.cannyImg.size[1] and pixel[1] > 0))
    
    def pixelIsEdge(self, pixel):
        if(self.cannyImage[pixel[0], pixel[1]] != (0,0,0)):
            return True
        return False

class SWTVector: 
    def __init__(self, startIn, endIn):
        self.start = startIn
        self.end = endIn
        self.dx = endIn[0]-startIn[0]
        self.dy = endIn[1]-startIn[1]
        self.magnitude = sqrt(self.dy**2 + self.dx**2)
        
    def getMagnitude(self):
        return self.magnitude

    def getMidpoint(self):
        return (self.start[0] + self.dx/2, self.start[1] + self.dy/2)
    
    def drawMidpointOntoImage(self, image, color):
        midpoint = self.getMidpoint()
        image[midpoint[0], midpoint[1]] = color
    
    def setMagnitudeAboutMidpoint(self, magnitudeIn):
        ratio = magnitudeIn/self.magnitude
        midpoint = self.getMidpoint()
        self.magnitude = magnitudeIn
        self.dx *= ratio
        self.dy *= ratio
        self.start = (midpoint[0] - self.dx/2.0, midpoint[1] - self.dy/2.0)
        self.end = (midpoint[0] + dx/2.0, midpoint[1] + self.dy/2.0)
        
    
    def __repr__(self):
        return "SWT: " + str(self.magnitude)
'''
Created on Feb 14, 2017

@author: phusisian
'''
import numpy
from root.nested.Vector import Vector
from math import sin, cos
from root.nested.Rectangle import Rectangle
from root.nested.Drawer import Drawer

class PolarSideCounter:
    
    def __init__(self, cannyImgIn, cannyImageIn):
        self.cannyImg = cannyImgIn
        self.cannyImage = cannyImageIn
        self.setOrigin()
        self.initPlot()
        self.maxWindow = 5
        self.appendWindowToPlot()
        self.setMean()
        '''not sure if it is good to set under mean to mean, because there may be a shape that does have
        legitimate maximums that are smaller than the mean'''
        #self.setUnderMeanToMean()
        self.smoothPlot(6, 6)
        
        self.initMaximums()

    
    def setOrigin(self):
        self.origin = (self.cannyImg.size[0]/2, self.cannyImg.size[1]/2)
    
    def initPlot(self):
        self.plot = []
        for x in range(0, self.cannyImg.size[0]):
            for y in range(0, self.cannyImg.size[1]):
                if self.cannyImage[x,y] == (255,255,255):#!= (0,0,0):
                    vectorFromCenter = Vector([x - self.origin[0], y - self.origin[1]])
                    self.plot.append(RadiusAngle(vectorFromCenter.getMagnitude(), vectorFromCenter.getTheta2D()))
        self.plot = sorted(self.plot, key = lambda angle: angle.getAngle())
        #self.plot = numpy.asarray(self.plot, dtype=RadiusAngle)
        
        '''print(self.plot)
        
        biggestR = 0
        biggestRIndex = 0
        for i in range(1, len(self.plot)):
            if self.plot[i].getRadius() > biggestR:
                biggestR = self.plot[i].getRadius()
                biggestRIndex = i
                
        print("biggest radius angle: " + str(self.plot[biggestRIndex].getAngle())) '''
    
    def appendWindowToPlot(self):
        endFirstSlice = self.plot[len(self.plot) - (self.maxWindow-1)/2 : len(self.plot)]
        beginLastSlice = self.plot[0: (self.maxWindow-1)/2]
        print("end first slice: " + str(endFirstSlice))
        for i in range(0, (self.maxWindow-1)/2):
            self.plot.insert(i, endFirstSlice[i])
        
        print("begin last slice: " + str(beginLastSlice))
        for i in range(0, len(beginLastSlice)):
            self.plot.append(beginLastSlice[i])
    
        print(self.plot)
        
    def setMean(self):
        #self.mean = numpy.average(self.plot)
        self.mean = 0
        for i in range(0, len(self.plot)):
            self.mean += self.plot[i].getRadius()
        #print("len plot " + str(len(self.plot)))
        self.mean = self.mean/float(len(self.plot))
        
    def setUnderMeanToMean(self):   
        for i in range(0, len(self.plot)):
            if self.plot[i].getRadius() < self.mean:
                self.plot[i].setRadius(self.mean)
    
    def smoothPlot(self, window, numTimes):
        for i in range(0, numTimes):
            for j in range((window-1)/2, len(self.plot) - window/2):
                self.plot[j].setRadius(self.getMeanInWindow(j, window))
                
    def getMeanInWindow(self, index, window):
        sum = 0
        windowCount = 0
        while windowCount < window:
            #print("window count: " + str(windowCount))
            '''if index - window/2 + windowCount >= len(self.plot):
                windowCount -= len(self.plot)'''
            sum += self.plot[index - window/2 + windowCount].getRadius()
            windowCount += 1
            
            #sum += self.plot[i].getRadius()
        return sum/float(window)

    def initMaximums(self):
        self.maximums = []
        #print(self.plot)
        for i in range((self.maxWindow-1)/2, len(self.plot) - (self.maxWindow-1)/2):
            if self.getIfIsMaxAcrossNum(i, self.maxWindow):
                self.maximums.append(self.plot[i])
                self.plot[i].drawDot(self.cannyImg, self.cannyImage, self.origin)
        print("size maximums: " + str(len(self.maximums)))
        print("maximums: " + str(self.maximums))
        self.cannyImg.show()
    
    
    def getIfIsMaxAcrossNum(self, index, num):
        indexCount = index - (num-1)/2
        #print("indexCount: " + str(indexCount))
        while indexCount < index - 1:
            if not(self.plot[indexCount].getRadius() < self.plot[indexCount + 1].getRadius()):
                return False
            indexCount += 1
            if indexCount >= len(self.plot):
                indexCount -= len(self.plot)
        indexCount = index
        
        while indexCount < index + (num-1)/2:
            #print("right called")
            if not(self.plot[indexCount].getRadius() > self.plot[indexCount + 1].getRadius()):
                return False
            indexCount += 1
            if indexCount >= len(self.plot):
                indexCount -= len(self.plot)
        #print()
        if not (self.plot[index].getRadius() > self.plot[index-1].getRadius() and self.plot[index].getRadius() > self.plot[index + 1].getRadius()):
            return False
        return True    
        
    def printNumMaximumsOverMaxMean(self):
        count = 0
        for i in range(0, len(self.maximums)):
            if self.maximums[i].getRadius() > self.maximumsMean:
                count += 1
        #print("revised side count: " + str(count))
            
        
class RadiusAngle:
    def __init__(self, radiusIn, angleIn):
        self.radius = radiusIn
        self.angle = angleIn
        
    def getRadius(self):
        return self.radius
    
    def setRadius(self, r):
        self.radius = r
    
    def getAngle(self):
        return self.angle    
    
    def sortKey(self):
        return self.angle
    
    def drawDot(self, img, image, center):
        dx = int(self.radius * cos(self.angle))
        dy = int(self.radius * sin(self.angle))
        rect = Rectangle(center[0]+dx - 4, center[1] + dy - 4, 8, 8)
        Drawer.fillRect(img, image, rect, (0,255,0))
        #image[center[0]+dx, center[1]-dy] = (0,255,0)
    
    def __repr__(self):
        return "Angle: " + str(self.angle) + " Radius: " + str(self.radius)
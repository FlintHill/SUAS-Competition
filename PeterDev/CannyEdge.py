'''
Created on Dec 2, 2016

@author: phusisian
'''

from root.nested.Point import Point
from PIL import Image
import math
from __builtin__ import True

class CannyEdge:
    
    @staticmethod
    def getCannyEdgeImageText(sobelEdge, upperThreshold, lowerThreshold):
        img = Image.new("RGB", (len(sobelEdge.getGradientsX()), len(sobelEdge.getGradientsX()[0])))
        image = img.load()
        dim = img.size
        
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if CannyEdge.isMaximumAcrossAngleText(sobelEdge, x, y) and sobelEdge.getSobelEdgeImage()[x,y][0] > upperThreshold:
                    image[x,y] = (255,255,255)
        
        
        #***currently no historeisis thresholding***
        return CannyEdge.getBasicThresholdedImg(img, image, sobelEdge.getMagGradients(), lowerThreshold)
        
        
        
    @staticmethod
    def getCannyEdgeImage(sobelEdge, upperThreshold, lowerThreshold):
        img = Image.new("RGB", (len(sobelEdge.getGradientsX()), len(sobelEdge.getGradientsX()[0])))
        image = img.load()
        dim = img.size
        
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if CannyEdge.isMaximumAcrossAngleText(sobelEdge, x, y) and sobelEdge.getSobelEdgeImage()[x,y][0] > upperThreshold:
                    image[x,y] = (255,255,255)
        
        
        #***currently no historeisis thresholding***
        
        return CannyEdge.getBasicThresholdedImg(img, image, sobelEdge.getMagGradients(), lowerThreshold)
         
      
    @staticmethod
    def isMaximumAcrossAngle(sobelEdge, x, y):
        dim = sobelEdge.getSobelEdgeImg().size
        if x > 0 and x < dim[0] - 1 and y > 0 and y < dim[1] - 1:
            perpAngle = sobelEdge.getAngles()[x][y] + (math.pi/4.0)
            sideColorOneNum = sobelEdge.getSobelEdgeImage()[int(x + round(math.cos(perpAngle))), int(y - round(math.sin(perpAngle)))][0]#check here if this messes up. Flopped all the y + and y - so that they fit the backwards y axis
            sideColorTwoNum = sobelEdge.getSobelEdgeImage()[int(x - round(math.cos(perpAngle))), int(y + round(math.sin(perpAngle)))][0]
            pixelColorNum = sobelEdge.getSobelEdgeImage()[x,y][0]
            
            #if (pixelColorNum >= sideColorOneNum and pixelColorNum > sideColorTwoNum) or (pixelColorNum > sideColorOneNum and pixelColorNum >= sideColorTwoNum):
            if(pixelColorNum > sideColorOneNum and pixelColorNum > sideColorTwoNum):
                return True
            
        return False  
         
    #def getThresholdPoints(self, sobelEdge, cannyImg, cannyImage, upperThreshold, lowerThreshold):
        
    @staticmethod
    def getPixelsToLookAcrossText(pixelIn, perpAngle):
        
        r = 1.5#1.618#experimenting with the radius can give different/better results
        
        xComp = r * math.cos(perpAngle)
        yComp = r * math.sin(perpAngle)
        dx = 0
        dy = 0
        val = r * math.sin((math.pi/8.0))
        #print("val: " + str(val))
        if yComp > -val and yComp < val:
            dy = 0
        elif yComp >= val:
            dy = 1
        elif yComp <= -val:
            dy = -1
            
        if xComp > -val and xComp < val:
            dx = 0
        elif xComp >= val:
            dx = 1
        elif xComp <= -val:
            dx = -1
        
        firstPixel = (pixelIn[0] + dx, pixelIn[1] - dy)
        secondPixel = (pixelIn[0] - dx, pixelIn[1] + dy)
        return (firstPixel, secondPixel)
        

    #Experiment with using check pixels not directly next to pixel (maybe rcos(angle), rsin(angle) where r = 2 or more)
    '''method exists because flat text will not have a maximum across one side of a possible edge because it is made up of an absolutely flat color with no variation'''
    @staticmethod
    def isMaximumAcrossAngleText(sobelEdge, x, y):
        dim = sobelEdge.getSobelEdgeImg().size
        if x > 0 and x < dim[0] - 1 and y > 0 and y < dim[1] - 1:
            perpAngle = sobelEdge.getAngles()[x][y] + (math.pi/4.0)
            #maxSide = math.sqrt(2)
            #sideColorOneNum = sobelEdge.getSobelEdgeImage()[int(x + round(math.cos(perpAngle))), int(y - round(math.sin(perpAngle)))][0]
            #sideColorTwoNum = sobelEdge.getSobelEdgeImage()[int(x - round(math.cos(perpAngle))), int(y + round(math.sin(perpAngle)))][0]
            
            #pixelSideOne = (x + math.cos(perpAngle), y - math.sin(perpAngle))
            #pixelSideTwo = (x - round(math.cos(perpAngle)), y + math.sin(perpAngle))
            #print("Pixel side one: " + str(pixelSideOne) + " Pixel side two: " + str(pixelSideTwo))
            
            #sideColorOneNum = sobelEdge.getSobelEdgeImage()[int(x + maxSide * math.cos(perpAngle)), int(y - maxSide * math.sin(perpAngle))][0]
            #sideColorTwoNum = sobelEdge.getSobelEdgeImage()[int(x - maxSide * math.cos(perpAngle)), int(y + maxSide * math.sin(perpAngle))][0]
            
            
            
            pixelColorNum = sobelEdge.getMagGradients()[x][y]
            
            pixelsToLookAcross = CannyEdge.getPixelsToLookAcrossText((x,y), perpAngle)
            sideColorOne = sobelEdge.getMagGradients()[pixelsToLookAcross[0][0]][pixelsToLookAcross[0][1]]
            sideColorTwo = sobelEdge.getMagGradients()[pixelsToLookAcross[1][0]][pixelsToLookAcross[1][1]]
            
            if (pixelColorNum >= sideColorOne and pixelColorNum >= sideColorTwo):# or (pixelColorNum >= sideColorOne and pixelColorNum > sideColorTwo):# or (pixelColorNum > sideColorOne and pixelColorNum >= sideColorTwo):
                return True
            
            #if (pixelColorNum >= sideColorOneNum and pixelColorNum > sideColorTwoNum) or (pixelColorNum > sideColorOneNum and pixelColorNum >= sideColorTwoNum):
            '''if(pixelColorNum > sideColorOneNum and pixelColorNum >= sideColorTwoNum):
                return True'''
            
        return False
    
    '''this can be called multiple times to fill in bigger gaps, but increases the possibility of faulty edges being found'''
    @staticmethod
    def getBasicThresholdedImg(img, image, magGradients, lowerThreshold):
        copyImg = img.copy()
        copyImage = copyImg.load()
        for x in range(1, img.size[0] - 1):
            for y in range(1, img.size[1] - 1):
                if image[x,y] != (255,255,255) and magGradients[x][y] >= lowerThreshold and CannyEdge.pixelSurroundedByEdges(image, (x,y), 3, 2):
                    copyImage[x,y] = (255,0,255)
        return copyImg
        
    @staticmethod
    def pixelSurroundedByEdges(image, pixel, kernelSize, minEdges):
        edgeCount = 0
        lastIndex = (-1,-1)
        for i in range(pixel[0] - (kernelSize/2), pixel[0] + 1 + kernelSize/2):
            for j in range(pixel[1] - (kernelSize/2), pixel[1] + 1 + kernelSize/2):
                if image[i,j] != (0,0,0):
                    if (abs(j - lastIndex[1]) + abs(i - lastIndex[0])) > 2:
                        edgeCount += 1  
                        lastIndex = (i,j)
                    
            
        return (edgeCount >= minEdges)
                
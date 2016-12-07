'''
Created on Dec 1, 2016

@author: phusisian
'''

from PIL import Image
import math
class GaussianBlur:
    
    @staticmethod
    def getGaussianFilteredImage(img, image, kernelSize):
        dim = img.size
        gaussianImg = Image.new("RGB", (dim[0] - (kernelSize - 1), dim[1] - (kernelSize - 1)))
        gaussianImage = gaussianImg.load()
        gaussianDim = gaussianImg.size
        
        for x in range(0, gaussianDim[0]):
            for y in range(0, gaussianDim[1]):
                gaussianImage[x,y] = GaussianBlur.getWeightedAverageColor(GaussianBlur.getColorsInKernel(image, kernelSize, x+(kernelSize - 1)/2, y+(kernelSize - 1)/2), kernelSize)
                
        return gaussianImg
      
    @staticmethod    
    def getColorsInKernel(image, kernelSize, midX, midY):
        colorList = [(0,0,0) for i in range(0, kernelSize **2)]
        numColorsCounted = 0
        for x in range(midX - ((kernelSize - 1)/2), midX + ((kernelSize + 1)/2)):
            for y in range(midY - ((kernelSize - 1)/2), midY + ((kernelSize + 1)/2)):
                colorList[numColorsCounted] = image[x,y]
                numColorsCounted += 1
        return colorList
    
    @staticmethod
    def getWeightedAverageColor(colors, kernelSize):
        gaussianFunction = GaussianBlur.getGaussianFunctionArray(GaussianBlur.getStandardDeviationOfColors(colors), kernelSize)
        addRed = 0
        addGreen = 0
        addBlue = 0
        
        for x in range(0, kernelSize):
            for y in range(0, kernelSize):
                addRed += colors[x*kernelSize + y][0] * gaussianFunction[0][x][y]
                addGreen += colors[x*kernelSize + y][1] * gaussianFunction[1][x][y]
                addBlue += colors[x*kernelSize + y][2] * gaussianFunction[2][x][y]
        
        addNums = [0 for i in range(0, len(gaussianFunction))]
        
        for i in range(0, len(addNums)):
            addNums[i] = GaussianBlur.addNumbersIn2DArray(gaussianFunction[i])
        
        return (int(float(addRed)/addNums[0]), int(float(addGreen)/addNums[1]), int(float(addBlue)/addNums[2]))
        
    
    @staticmethod
    def addNumbersIn2DArray( array):
        addNum = 0
        for i in range(0, len(array)):
            for j in range(0, len(array[0])):
                addNum += array[i][j]
        return addNum
        
    @staticmethod   
    #average color is split from standard deviation even though one is needed to do the other. Would be faster to conjoin 
    def getAverageColor( colors):
        addRed = 0
        addGreen = 0
        addBlue = 0
        for i in range(0, len(colors)):
            addRed += colors[i][0]
            addGreen += colors[i][1]
            addBlue += colors[i][2]
        return (int(addRed/float(len(colors))) + 1, int(addGreen/float(len(colors))) + 1, int(addBlue/float(len(colors))) + 1) #adding one to the end is a bit of a hack so the standard deviation is never zero so you don't get divide by zero error. Either way, if casting to int, I don't think you can get out of bounds color because it rounds down (unless it exactly adds up to 255?)
    
    @staticmethod
    def getStandardDeviationOfColors(colors):
        averageColor = GaussianBlur.getAverageColor(colors)
        average = GaussianBlur.getMagnitudeOfColor(averageColor)
        stdAddRed = 0
        stdAddGreen = 0
        stdAddBlue = 0
        
        for i in range(0, len(colors)):
            #print(colors[i])
            stdAddRed += (colors[i][0] - averageColor[0])**2
            stdAddGreen += (colors[i][1] - averageColor[1])**2
            stdAddBlue += (colors[i][2] - averageColor[2])**2
            
        stdAddRed = math.sqrt(float(stdAddRed)/float(len(colors)))
        stdAddGreen = math.sqrt(float(stdAddGreen)/float(len(colors)))
        stdAddBlue = math.sqrt(float(stdAddBlue)/float(len(colors)))
        '''print("stdAddRed: " + str(stdAddRed))
        print("stdAddBlue: " + str(stdAddBlue))
        print("stdAddGreen: " + str(stdAddGreen))'''
        return(stdAddRed, stdAddGreen, stdAddBlue)
    
    @staticmethod    
    def getGaussianFunctionArray( standardDeviation, kernelSize):
        gaussianFunctionArray = [[[0 for i in range(0, kernelSize)] for j in range(0, kernelSize)] for k in range(0, len(standardDeviation))]
        
        for x in range(0, kernelSize):
            for y in range(0, kernelSize):
                for i in range(0, len(standardDeviation)):
                    #if standardDeviation[i] > 0:
                    gaussianFunctionArray[i][x][y] = (1.0/(2.0 * math.pi * standardDeviation[i]**2))
                    gaussianFunctionArray[i][x][y] *= math.exp(-( x - (((kernelSize-1)/2) )**2 + (y - ((kernelSize -1)/2)))/(2*(standardDeviation[i])**2) )
                    
        return gaussianFunctionArray
    
    @staticmethod    
    def getMagnitudeOfColor( color):
        return math.sqrt(color[0]**2 + color[1]**2 + color[2]**2)
    
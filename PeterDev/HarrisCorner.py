from PIL import Image
from root.nested.Drawer import Drawer
from root.nested.Rectangle import Rectangle
from root.nested.GaussianBlur import GaussianBlur
from math import sqrt
from root.nested.Point import Point
from math import atan2
from math import pi
import math
from __builtin__ import False
class HarrisCorner:
    '''assumes a grayscaled image'''
    A_CONSTANT = 0.1
    @staticmethod
    def getCorners(img, image, sobelEdge, kernelSize, stdDev, threshold):
        cornerScores = [[0 for j in range(img.size[1])] for i in range(0, img.size[0])]
        kernel = GaussianBlur.getGaussianKernel(kernelSize, stdDev)
        initOffset = (kernelSize - 1)/2
        gradientsX = sobelEdge.getGradientsX()
        gradientsY = sobelEdge.getGradientsY()
        for x in range(initOffset, len(cornerScores) - initOffset):
            for y in range(initOffset, len(cornerScores[0]) - initOffset):
                momentMatrix = HarrisCorner.getSecondMomentMatrix(kernel, Point(x,y), gradientsX, gradientsY)
                cornerScore = HarrisCorner.getHarrisOutput(momentMatrix)
                cornerScores[x][y] = cornerScore
        harrisCorners = []
        for x in range(1, img.size[0] - 1):
            for y in range(1, img.size[1] - 1):
                if cornerScores[x][y] > threshold:
                    paintRect = Rectangle(x-initOffset, y-initOffset, kernelSize, kernelSize)
                    if HarrisCorner.isMaxAcrossEdge(sobelEdge, Point(x,y), cornerScores):
                        addPointBool = True
                        for harrisCorner in harrisCorners:
                            if harrisCorner.getIfXYInKernel((x, y)):
                                addPointBool = False
                        if addPointBool == True:
                            harrisCorners.append(Corner((x,y), kernelSize))
                        #Drawer.fillRect(img, image, paintRect, (255,0,0))
                  
        return harrisCorners
    
    @staticmethod
    def checkIfRectContainsRed(image, rect):
        redFound = False
        for x in range(rect.getX(), rect.getX() + rect.getWidth()):
            for y in range(rect.getY(), rect.getY() + rect.getHeight()):
                if image[x,y] == (255,0,0):
                    redFound = True
        return redFound
    
    @staticmethod
    def isMaxAcrossEdge(sobelEdge, pixelPoint, cornerScores):
        perpAngle = sobelEdge.getAngles()[pixelPoint.getX()][pixelPoint.getY()] + (pi/4.0)#atan2(gradientsY[pixelPoint.getX()][pixelPoints.getY()], gradientsX[pixelPoint.getX()][pixelPoint.getY()])
        cornerOneScore = cornerScores[int(pixelPoint.getX() + round(math.cos(perpAngle)))][int(pixelPoint.getY() + round(math.sin(perpAngle)))]
        cornerTwoScore = cornerScores[int(pixelPoint.getX() - round(math.cos(perpAngle)))][int(pixelPoint.getY() - round(math.sin(perpAngle)))]
        return(cornerScores[pixelPoint.getX()][pixelPoint.getY()] > cornerOneScore and cornerScores[pixelPoint.getX()][pixelPoint.getY()] > cornerTwoScore)
        
    @staticmethod
    def getSecondMomentMatrix(kernel, pixelPoint, gradientsX, gradientsY):
        h = [[0 for i in range(0, 2)] for j in range(0, 2)]
        initOffset = (len(kernel)-1)/2
        kernelX = 0
        kernelY = 0
        for x in range(pixelPoint.getX() - initOffset, pixelPoint.getX() + initOffset + 1):
            for y in range(pixelPoint.getY() - initOffset, pixelPoint.getY() + initOffset + 1):
                h[0][0] += kernel[kernelX][kernelY] * gradientsX[x][y]**2
                h[1][0] += kernel[kernelX][kernelY] * gradientsX[x][y] * gradientsY[x][y]
                h[0][1] += kernel[kernelX][kernelY] * gradientsX[x][y] * gradientsY[x][y]
                h[1][1] += kernel[kernelX][kernelY] * gradientsY[x][y]**2
                kernelY += 1
            kernelY = 0
            kernelX += 1
        return h
    '''
    @staticmethod
    def getLambdas(momentMatrix):
        #returns only the positive eigenvalue
        lambdaPositive = 0.5 * ((momentMatrix[0][0] + momentMatrix[1][1]) + sqrt(4*momentMatrix[0][1]*momentMatrix[1][0] + (momentMatrix[0][0] - momentMatrix[1][1]**2) ))
        lambdaNegative = 0.5 * ((momentMatrix[0][0] + momentMatrix[1][1]) - sqrt(4*momentMatrix[0][1]*momentMatrix[1][0] + (momentMatrix[0][0] - momentMatrix[1][1]**2) ))
        return (lambdaNegative, lambdaPositive)
    '''
    @staticmethod
    def getHarrisOutput(momentMatrix):
        #numerator = momentMatrix[0][0]*momentMatrix[1][1] - momentMatrix[0][1]*momentMatrix[1][0]
        #denominator = (momentMatrix[0][0] + momentMatrix[1][1])**2
        determinant = momentMatrix[0][0]*momentMatrix[1][1] - momentMatrix[0][1]*momentMatrix[1][0]
        trace = momentMatrix[0][0] + momentMatrix[1][1]
        output = determinant - HarrisCorner.A_CONSTANT*(trace**2)
        return output

class Corner:
    '''kernels could take a radius rather than a kernel size so it's adjustable the area in which another
    corner can't be placed'''
    def __init__(self, xy, kernelSize):
        self.xy = xy
        self.kernelSize = kernelSize
        
    def getIfXYInKernel(self, xy):
        initOffset = (self.kernelSize - 1)/2
        return (xy[0] >= self.xy[0] - initOffset and xy[0] <= self.xy[0] + initOffset + 1 and xy[1] >= self.xy[1] - initOffset and xy[1] <= self.xy[1] + initOffset + 1)
            
    def __getitem__(self, index):
        return xy[index]      
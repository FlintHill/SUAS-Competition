from PIL import Image
import numpy
import math
from root.nested.CannyEdge import CannyEdge

class SobelEdge:
    global sobelKernelX, sobelKernelY;
    sobelKernelX = [[-1,0,1],[-2,0,2],[-1,0,1]]
    sobelKernelY = [[-1,-2,-1],[0,0,0],[1,2,1]]
    
    
    
    def __init__(self, imgIn, imageIn):
        self.image = imageIn
        self.img = imgIn
        self.setImageGradients()
        self.setSobelEdgeImg() 
        self.setAngles()
        
    '''@classmethod
    def getResizedSobelEdge(cls, sobelEdgeIn, sizeRect):
        newImg = sobelEdgeIn.getImg().resize((sizeRect.getWidth(), sizeRect.getHeight()), Image.BILINEAR)
        newImage = newImg.load()
        newImg.show()
        return SobelEdge(newImg, newImage)
      '''  
        
    def setImageGradients(self):
        gradients = numpy.zeros( (2, self.img.size[0], self.img.size[1]) )#[0 for i in range(0, len(sobelKernel))][0 for j in range(0, img.size[0])][0 for k in range(0, img.size[1])]
        
        for x in range(1, self.img.size[0] - 1):
            for y in range(1, self.img.size[1] - 1):
                appliedKernels = self.getAppliedKernels(x, y)
                gradients[0][x][y] = appliedKernels[0]
                gradients[1][x][y] = appliedKernels[1]
        
        self.gradients = gradients
        #self.gradientsX = gradients[0]
        #self.gradientsY = gradients[1]
                
                
    def setSobelEdgeImg(self):
        #print(len(gradients[0]))
        #print(len(gradients[0][0]))
        outputImage = Image.new("RGB", (len(self.gradients[0]), len(self.gradients[0][0])))
        image = outputImage.load()
        
        for x in range(0, outputImage.size[0]):
            for y in range(0, outputImage.size[1]):
                magColor = int(math.sqrt( (self.gradients[0][x][y])**2 + (self.gradients[1][x][y])**2 ))
                image[x,y] = (magColor, magColor, magColor)
        
        self.sobelEdgeImg = outputImage
        self.sobelEdgeImage = image
        

    #Worth noting that many methods in this class are hard-coded to a 3x3 dimension of the sobel kernel
    def getAppliedKernels(self, pixelX, pixelY):
        appliedKernelSum = [0 for i in range(0,2)]
        for i in range(0, len(sobelKernelX)):
            for j in range(0, len(sobelKernelX)):
                appliedKernelSum[0] += (sobelKernelX[i][j])*self.image[pixelX - 1 + i, pixelY - 1 + j][0]
                appliedKernelSum[1] += (sobelKernelY[i][j])*self.image[pixelX - 1 + i, pixelY - 1 + j][0]
        return appliedKernelSum        
        
    def getImg(self):
        return self.img    
        
    def getSobelEdgeImg(self):
        return self.sobelEdgeImg      
    
    def getSobelEdgeImage(self):
        return self.sobelEdgeImage
    
    def getGradientsX(self):
        return self.gradients[0]
    
    def getGradientsY(self):
        return self.gradients[1]
    
    def getAngles(self):
        return self.angles
    
    def setAngles(self):
        self.angles = [[0 for i in range(0, len(self.gradients[0][0]))] for j in range(0, len(self.gradients[0]))]
        for x in range(0, len(self.angles)):
            for y in range(0, len(self.angles[0])):
                self.angles[x][y] = math.atan2(self.gradients[1][x][y], self.gradients[0][x][y])
                
    def getAnglesAtRow(self, index, threshold):
        angleReturn = []
        if len(self.angles[0]) > index:
            for i in range(0, len(self.angles)):
                if self.sobelEdgeImage[i, index] > (threshold, threshold, threshold): #THIS IS THRESHOLDABLE, when set to > 0, accuracy was worse than when set to > 30, for example
                    angleReturn.append(self.angles[i][index])
                    
        return angleReturn
    
    def printAngles(self):
        for i in range(0, len(self.angles[0])):
            print(self.getAnglesAtRow(i))
    
    def getAngleImage(self, threshold):
        img = Image.new("RGB", self.sobelEdgeImg.size)
        image = img.load()
        dim = img.size
        sobelEdgeImage = self.sobelEdgeImg.load()
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if sobelEdgeImage[x,y] >= (threshold, threshold, threshold):
                    red = int((math.sin(self.angles[x][y]) + 1)*122)
                    green = int((math.sin(self.angles[x][y] + (2*math.pi/3.0)) + 1)*122)
                    blue = int((math.sin(self.angles[x][y] + (4*math.pi/3.0)) + 1)*122)
                    image[x,y] = (red, green, blue)
        return img
                    
                
                
    
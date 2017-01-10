'''
Created on Dec 2, 2016

@author: phusisian
'''
from root.nested.Rectangle import Rectangle
from PIL import Image
from root.nested.ImageOperations import ImageOperations
from root.nested.Point import Point
from root.nested.KMeans import KMeans

class ColorLayer:
    
    #***this is written confusingly. One would assume it would split an image into its color layer itself, not create an image for that to occur in by another function***
    def __init__ (self, img, image, color, x = -1, y = -1):
        self.colorImg = img
        self.colorImage = self.colorImg.load()
        if x != -1 and y != -1:
            self.colorImage[x,y] = color
        self.color = color
        
    @classmethod
    def initWithoutImg(cls, dim, color, x, y):
        newImg = Image.new("RGB", dim)
        return ColorLayer(newImg, newImg.load(), color, x, y)
    
    def removeLayerFromImg(self, img, image):
        dim = img.size
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if self.colorImage[x,y] != (0,0,0):
                    image[x,y] = (0,0,0)
        return img
    
    def getPointsOfGreatestConcentration(self, numPoints, timesToRun = 10, step = 1):#represented as tuple, which could be confusing (not a point)
        data = self.toTuples()
        kMeans = KMeans(data, numPoints, timesToRun, step)
        clusterTuples = kMeans.getIntClusterVectors()
        return clusterTuples
    
    def getClusterOfGreatestConcentration(self, numPoints, timesToRun = 10, step = 1):#represented as tuple, which could be confusing (not a point)
        data = self.toTuples()
        kMeans = KMeans(data, numPoints, timesToRun, step)
        clusterTuples = kMeans.getClusters()[0]
        
        return clusterTuples    
    
    def toTuples(self):
        tuples = []
        bounds = self.getColorLayerBounds()
        for x in range(bounds.getX(), bounds.getX() + bounds.getWidth()):
            for y in range(bounds.getY(), bounds.getY() + bounds.getHeight()):
                if(x > 0 and x < self.colorImg.size[0] and y > 0 and y < self.colorImg.size[1]):
                    if self.colorImage[x,y] != (0,0,0):
                        tuples.append((x,y))
        return tuples
    
    def getDensity(self):
        return float(self.getLayerPixelArea())/float(self.getLayerImageArea())
    
    def fillWithLayer(self, layer):
        for x in range(0, layer.getColorImg().size[0]):
            for y in range(0, layer.getColorImg().size[1]):
                if layer.getColorImage()[x,y] != (0,0,0):
                    self.colorImage[x,y] = self.color
                #self.colorImage[x,y] = (self.color) if layer.getColorImage()[x,y] != (0,0,0) else self.colorImage[x,y]
            
    
    def getLayerPixelArea(self):
        count = 0
        for x in range(0, self.colorImg.size[0]):
            for y in range(0, self.colorImg.size[1]):
                count += 1 if self.colorImage[x,y] != (0,0,0) else 0
        return count
    
    def getLayerImageArea(self):
        return self.colorImg.size[0] * self.colorImg.size[1]
    
    def drawPixel(self, color, x, y):
        self.colorImage[x,y] = color
    
    def getColor(self):
        return self.color
    
    def getColorImg(self):
        return self.colorImg
    
    def getColorImage(self):
        return self.colorImage
    
    def getColorLayerBounds(self):
        dim = self.colorImg.size
        
        leftX = dim[0]
        rightX = 0
        topY = dim[1]
        bottomY = 0
        
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if self.colorImage[x,y] != (0,0,0):
                    if x < leftX:
                        leftX = x
                    if x > rightX:
                        rightX = x
                    if y < topY:
                        topY = y 
                    if y > bottomY:
                        bottomY = y
        '''if leftX >= 3:
            leftX -= 3
        if rightX <= dim[0] - 6:
            rightX += 6
        if topY >= 3:
            topY -= 3
        if bottomY <= dim[1] - 4:
            bottomY += 4'''
        
        if leftX >= 3:
            leftX -= 3
            #if rightX <= self.colorImg.size[0] - 5:
            rightX += 5
                
        if topY >= 3:
            topY -= 3
            #if bottomY <= self.colorImg.size[1] - 5:
            bottomY += 5
        
        return Rectangle(leftX, topY, rightX - leftX, bottomY - topY)
    
    def getIfXYInLayer(self, x, y):
        if(x > 0 and x < self.colorImg.size[0] and y > 0 and y < self.colorImg.size[1]):
            return (self.colorImage[x,y] != (0,0,0))
        return False
    
    def getColorLayerBoundsMidpoint(self):
        rect = self.getColorLayerBounds()
        returnPoint = Point((rect.getX() + rect.getWidth())/2, (rect.getY() + rect.getHeight())/2)
        return returnPoint
    
    def getColorLayerBoundsCorner(self):
        rect = self.getColorLayerBounds()
        return Point(rect.getX(), rect.getY())
    
    def cropLayerToBounds(self):
        self.colorImg = ImageOperations.cropToRectangle(self.colorImg, self.getColorLayerBounds())
        self.colorImage = self.colorImg.load()
    
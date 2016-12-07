from root.nested.Point import Point
from math import sqrt
from PIL import Image
class ColorLayers:
    def __init__ (self, img, image):
        self.colorLayers = []
        self.img = img
        self.image = image
        self.fillHoles()
      
    def __getitem__(self, index):
        return self.colorLayers[index]  
    
    def __len__(self):
        return len(self.colorLayers)

    def __setitem__(self, index, value):
        self.colorLayers[index] = value

    def pop(self, index):
        self.colorLayers.pop(index)

    def append(self, colorLayer):
        self.colorLayers.append(colorLayer)
      
    def sortLayersByDistanceToCorner(self):
        for i in range(0, len(self)):
            smallestIndex = i
            smallestDist = self.getDistanceToMidpoint(self[i].getColorLayerBoundsCorner())
            for j in range(i+1, len(self)):
                distCalc = self.getDistanceToMidpoint(self[j].getColorLayerBoundsCorner())
                if distCalc < smallestDist:
                    smallestDist = distCalc
                    smallestIndex = j
            
            tempLayer = self[i]
            self[i] = self[smallestIndex]
            self[smallestIndex] = tempLayer
    
    def overlayLayersOntoImg(self, imgIn):
        returnImg = imgIn.copy()
        for i in range(0, len(self)):
            returnImg.paste(self[i].getColorImg(), (0,0), self[i].getColorImg())
        return returnImg
    
    
    def fillHoles(self):
        i = len(self)
        while i > 1:
            self[i-1].fillWithLayer(self[i])
            i -= 1
    
    def getDensestColorLayer(self):
        print("Len: " + str(len(self)))
        densestIndex = 0
        bigDensity = self[0].getDensity()
        print(bigDensity)
        for i in range(1, len(self)):
            compareDensity = self[i].getDensity()
            
            if compareDensity > bigDensity:
                print(str(compareDensity) + ", " + str(bigDensity))
                bigDensity = compareDensity
                densestIndex = i
        return self[densestIndex]
    
    def printLayerDistancesToCorner(self):
        for i in range(0, len(self)):
            print(str(self.getDistanceToMidpoint(self[i].getColorLayerBoundsCorner())))
    
    def getDistanceToMidpoint(self, pointIn):
        midpoint = self.getMidpoint()
        return sqrt((pointIn.getX() - midpoint.getX())**2 + (pointIn.getY() - midpoint.getY())**2)
        
    def getMidpoint(self):
        midpoint = Point(self.img.size[0]/2, self.img.size[1]/2)
        return midpoint
    
      
    def getIndexOfColor(self, color):
        for i in range(0, len(self.colorLayers)):
            if self.colorLayers[i].getColor() == color:
                return i
        return -1
     
    '''def getLayerAtIndex(self, index):
        return self.colorLayers[index]'''
     
    '''def getLayers(self):
        return self.colorLayers'''
    
    def showColorLayers(self):
        for i in range(0, len(self.colorLayers)):
            self.colorLayers[i].getColorImg().show()
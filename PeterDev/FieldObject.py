'''
Created on Dec 6, 2016

@author: phusisian
'''
from root.nested.SobelEdge import SobelEdge
from root.nested.ColorLayers import ColorLayers
from root.nested.ColorLayer import ColorLayer
from root.nested.Drawer import Drawer
from root.nested.ColorSeparation import ColorSeparation
from root.nested.Rectangle import Rectangle
from root.nested import KMeans
from root.nested.ImageOperations import ImageOperations
import PIL
import math
from root.nested.GaussianBlur import GaussianBlur
from root.nested.GrayScale import GrayScale
from root.nested.LetterFrames import LetterFrames
from itertools import count
class FieldObject:

    def __init__(self, letterFramesIn, img, image):
        self.letterFrames = letterFramesIn#LetterFrames("Dual-300.ttf", 48)
        self.rotation = 45
        self.img = img
        self.img = self.img.rotate(self.rotation)
        self.image = self.img.load()
        imgCopy= self.img.copy()
        kMeans = KMeans.KMeans.initWithPicture(self.img, self.image, 3, 20)
        self.kMeansImg = kMeans.filterImageThroughClusters(imgCopy, imgCopy.load())
        self.kMeansImage = self.kMeansImg.load()
        #self.sobelEdge = SobelEdge(self.img, self.image)
        #self.kMeans = KMeans.initWithPicture(img, image, 3, 12)#12 is toggleable -- num times KMeans runs
        self.colorLayers = ColorSeparation.getColorLayers(self.kMeansImg, self.kMeansImage)
        self.colorLayers.sortLayersByDistanceToCorner()
        #letterImg = self.removeLayersUntilLetter()
        self.removeBackground()
        self.colorRounder = ColorRounder()
        self.letterCropper = LetterCropper(self.getLetterLayerCrappyVersion())
        
        self.sideCounter = SideCounter(self.getObjectColorLayer())
        
    
    def __repr__(self):
        bestFitLetter = self.getBestFitLetterFrame()
        return ("Color: " + self.getObjectColorName() +
        "\nShape: " + str(SideRounder.getShapeType(self.sideCounter.getNumSides())) + 
        "\nLetter: " + bestFitLetter.getLetter() + 
        "\nRotation: " + AngleCaster.castAngleToCompass(self.rotation))
    
    def getBestFitLetter(self):
        return self.getBestFitLetterFrame().getLetter()
    
    def getBestFitLetterFrame(self):
        return self.letterFrames.getBestFitLetterFrameFromSobel(self.letterCropper.getSobelEdge(), 25)
    
    def removeBackground(self):#could make this iterable if for some reason I have more than 3 colors 
        self.kMeansImg = self.colorLayers[len(self.colorLayers) - 1].removeLayerFromImg(self.kMeansImg, self.kMeansImage)
        self.colorLayers.pop(len(self.colorLayers) - 1)
        
    def getObjectColor(self):
        return self.getObjectColorLayer().getColor()
    
    def getObjectColorName(self):
        return self.colorRounder.getBestFitColorName(self.getObjectColor())
    
    def getObjectColorLayer(self):
        return self.colorLayers.getDensestColorLayer()   
        
    def getColorLayers(self):
        return self.colorLayers
    
    def getLetterSobel(self):
        return self.letterCropper.getSobelEdge()

    def getLetterLayerCrappyVersion(self):
        objectLayer = self.getObjectColorLayer()
        for i in range(0, len(self.colorLayers)):
            if self.colorLayers[i] != objectLayer:
                return self.colorLayers[i]
    
class LetterCropper:
    def __init__(self, letterLayer):
        self.letterLayer = letterLayer
        self.cluster = letterLayer.getClusterOfGreatestConcentration(1, 10)
        self.increment = .03
        self.fillDensityFunction(self.increment)
        self.fillMinimumsOfDensityFunction()
        self.fillMaximumsOfDensityFunction()
        imgCopy = letterLayer.getColorImg()
        #Drawer.drawCircle(imgCopy, imgCopy.load(), self.cluster.getIntClusterVector(), self.getGreatestGapBetweenMaximums()[0]*self.increment, (0,255,0), 500)
        self.croppedImg = self.getCroppedImageToRadius(self.getGreatestGapBetweenMaximums()[0]*self.increment)
        ratio = float(LetterFrames.frameHeight)/float(self.croppedImg.size[1])
        print("Ratio: " + str(ratio))
        self.croppedImg = self.croppedImg.resize((int(self.croppedImg.size[0]*ratio), int(self.croppedImg.size[1]*ratio)), PIL.Image.ANTIALIAS)
        fillRectangle = Rectangle(0, 0, 20, self.croppedImg.size[1])
        #Drawer.fillRect(self.croppedImg, self.croppedImg.load(), fillRectangle, (0,0,0))
        newColorLayer = ColorLayer(self.croppedImg, self.croppedImg.load(), (255,255,255))
        newColorLayer.cropLayerToBounds()
        self.croppedImg = newColorLayer.getColorImg()
        self.croppedImg = GrayScale.getGrayScaledImage(self.croppedImg, self.croppedImg.load())
        self.croppedImg = GaussianBlur.getGaussianFilteredImage(self.croppedImg, self.croppedImg.load(), 3)
        self.sobelEdge = SobelEdge(self.croppedImg, self.croppedImg.load())
        
    def getSobelEdge(self):
        return self.sobelEdge
        
    def fillDensityFunction(self, increment):
        self.densityFunction = []
        maxRadius = math.sqrt((self.letterLayer.getColorImg().size[0]/2.0)**2 + (self.letterLayer.getColorImg().size[1]/2.0)**2)#temporary jank. replace with greatest possible distance from cluster point to corner of image
        
        radius = 0
        while radius < maxRadius:
            self.densityFunction.append(self.cluster.getDataDensityInRadius(radius))
            radius += increment
            
    def getCroppedImg(self):
        return self.croppedImg        
    
    def fillMinimumsOfDensityFunction(self):
        self.minimumDensityLocations = []
        for i in range(1, len(self.densityFunction) - 1):
            if self.densityFunction[i-1] > self.densityFunction[i] and self.densityFunction[i+1] > self.densityFunction[i]:
                self.minimumDensityLocations.append(i)
    
    def fillMaximumsOfDensityFunction(self):
        self.maximumDensityLocations = []
        for i in range(1, len(self.densityFunction) - 1):
            if self.densityFunction[i-1] < self.densityFunction[i] and self.densityFunction[i+1] < self.densityFunction[i]:
                self.maximumDensityLocations.append(i)
    
    def getMiddleBetweenPoints(self, points):
        return points[0] + (points[1] - points[0])/2.0
    
    def getGreatestGapBetweenMaximums(self):
        greatestIndex = 0
        greatestGap = self.maximumDensityLocations[1] - self.maximumDensityLocations[0]
        for i in range(1, len(self.maximumDensityLocations) - 1):
            gap = self.maximumDensityLocations[i+1] - self.maximumDensityLocations[i]
            
            if gap >= greatestGap:
                print("Greater gap found")
                greatestGap = gap
                greatestIndex = i
                
        return (self.maximumDensityLocations[greatestIndex], self.maximumDensityLocations[greatestIndex + 1])
    
    def getMinimumBetweenMaximums(self, maximums):
        for i in range(0, len(self.minimumDensityLocations)):
            if self.minimumDensityLocations[i] > maximums[0] and self.minimumDensityLocations[i] < maximums[1]:
                return self.minimumDensityLocations[i]
    
    
    
    def getCroppedImageToRadius(self, radius):
        colorLayerCloneImg = self.letterLayer.getColorImg().copy()
        rect = Rectangle(int(self.cluster.getIntClusterVector()[0] - radius), int(self.cluster.getIntClusterVector()[1] - radius), int(radius * 2), int(radius * 2))
        colorLayerCloneImg = ImageOperations.cropToRectangle(colorLayerCloneImg, rect)
        return colorLayerCloneImg
    
class SideCounter:
    def __init__(self, sideLayer):
        self.sideLayer = sideLayer
        self.boundingRect = self.sideLayer.getColorLayerBounds()
        self.densestPoint = self.boundingRect.getMidpoint()#self.sideLayer.getPointsOfGreatestConcentration(1)[0]
        #self.boundingRect = self.sideLayer.getColorLayerBounds()
        self.numSides = self.countSides()
        
     
    def getNumSides(self):
        return self.numSides
    #Fuzzy edges lead to this being inaccurate because it could clip in and outside a noisy edge and count it as a side.  
    #Solution is to decrease number of steps, but then it could be possible it skips sides entirely (especially on very acute angles)  
    def countSides(self, numSteps = 64):
        thetaAdd = 2*math.pi/float(numSteps)
        theta = thetaAdd
        radius = self.getRadius() #the constant subtracted NEEDS to be as low as possible. Radius needs to be small enough to actually go under all points of the shape.
        previousIn = self.sideLayer.getIfXYInLayer(radius, 0)
        count = 0
        while theta < 2*math.pi:
            currentIn = self.sideLayer.getIfXYInLayer(int(self.densestPoint[0] + radius * math.cos(theta)), int(self.densestPoint[1] + radius * math.sin(theta)))
            if currentIn != previousIn:
                previousIn = currentIn
                count += 1
            
            theta += thetaAdd
    
    
        return count/2
    
    def getRadius(self):
        if self.boundingRect.getWidth() > self.boundingRect.getHeight():
            return self.boundingRect.getWidth()/2.0
        else:
            return self.boundingRect.getHeight()/2.0
    
class ColorRounder:
    def __init__(self):
        self.clusters = KMeans.Clusters()
        self.clusters.append(KMeans.Cluster((0,0,0)), "black")
        self.clusters.append(KMeans.Cluster((255,255,255)), "white")
        self.clusters.append(KMeans.Cluster((128,128,128)), "gray")
        self.clusters.append(KMeans.Cluster((255,0,0)), "red")
        self.clusters.append(KMeans.Cluster((0,255,0)), "blue")
        self.clusters.append(KMeans.Cluster((0,0,255)), "green")
        self.clusters.append(KMeans.Cluster((255,255,0)), "yellow")
        self.clusters.append(KMeans.Cluster((128,0,128)), "purple")
        self.clusters.append(KMeans.Cluster((165,42,42)), "brown")
        self.clusters.append(KMeans.Cluster((255,165,0)), "orange")
        
    def getBestFitColorName(self, colorIn):
        return self.clusters.getSmallestDistanceCluster(colorIn).getName()
   
class AngleCaster:
    angleArray = ["East", "North-East", "North", "North-West", "West", "South-West", "South", "South-East"]
    @staticmethod
    def castAngleToCompass(angle):
        return AngleCaster.angleArray[int((angle/(math.pi/4.0))%8)]
    
class SideRounder:
    #Eventually, rounds to shapes based on special characteristics (e.g. rectangle to square), currently only returns simple values
    shapeArray = [("triangle", 3), ("square", 4), ("pentagon", 5), ("hexagon", 6), ("heptagon", 7), ("octagon", 8)]
    
    @staticmethod
    def getShapeType(numSides):
        for i in range(0, len(SideRounder.shapeArray)):
            if SideRounder.shapeArray[i][1] == numSides:
                return SideRounder.shapeArray[i][0]
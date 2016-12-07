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
from math import sqrt
import PIL
from root.nested.GaussianBlur import GaussianBlur
from root.nested.GrayScale import GrayScale
from root.nested.LetterFrames import LetterFrames
class FieldObject:

    def __init__(self, img, image):
        
        img.show()
        self.img = img
        self.img = self.img.rotate(45)
        self.image = self.img.load()
        imgCopy= self.img.copy()
        kMeans = KMeans.KMeans.initWithPicture(self.img, self.image, 3, 20)
        self.kMeansImg = kMeans.filterImageThroughClusters(imgCopy, imgCopy.load())
        self.kMeansImage = self.kMeansImg.load()
        #self.sobelEdge = SobelEdge(self.img, self.image)
        #self.kMeans = KMeans.initWithPicture(img, image, 3, 12)#12 is toggleable -- num times KMeans runs
        self.colorLayers = ColorSeparation.getColorLayers(self.kMeansImg, self.kMeansImage)
        self.colorLayers.sortLayersByDistanceToCorner()
        #self.colorLayers.showColorLayers()
        #letterImg = self.removeLayersUntilLetter()
        self.removeBackground()
        self.colorRounder = ColorRounder()
        self.letterCropper = LetterCropper(self.getLetterLayerCrappyVersion())
        self.letterCropper.getCroppedImg().show()
        #self.colorLayers.showColorLayers()
        #letterImg.show()
    
    
    def removeBackground(self):#could make this iterable if for some reason I have more than 3 colors 
        #self.img.show()
        #self.img = self.colorLayers[len(self.colorLayers) - 1].removeLayerFromImg(self.img, self.image)
        self.kMeansImg = self.colorLayers[len(self.colorLayers) - 1].removeLayerFromImg(self.kMeansImg, self.kMeansImage)
        #self.img.show()
        #self.colorLayers[len(self.colorLayers) - 1].getColorImg().show()
        self.colorLayers.pop(len(self.colorLayers) - 1)
        #self.img.show()
        
        #for i in range(0, len(self.colorLayers)):
        '''    
        pointTuples = self.colorLayers[1].getPointsOfGreatestConcentration(150, 10)
        for j in range(0, len(pointTuples)):
            rect = Rectangle(pointTuples[j][0] - 2, pointTuples[j][1] - 2, 4, 4)
            Drawer.fillRect(self.img, self.image, rect, (0,255,0))
    
        self.img.show()'''
        
        '''copyImg = self.img.copy()
        copyImg.show()
        kMeans = KMeans.initWithPicture(copyImg, copyImg.load(), 2, 20)
        copyImg.show()
        kMeansImg2 = kMeans.filterImageThroughClusters(copyImg, copyImg.load())
        kMeansImg2.show()
        newColorLayers = ColorSeparation.getColorLayers(kMeansImg2, kMeansImg2.load())
        newColorLayers.sortLayersByDistanceToCorner()
        letterImg = newColorLayers[len(newColorLayers) - 1].removeLayerFromImg(self.img, self.image)
        letterImg.show()
        self.img.show()'''
    '''def showLayerImg(self):
        self.colorLayers.overlayLayersIntoImg().show()'''
    
    '''def getLetterColorLayer(self):
        self.colorLayers[0].getColorImg().show()
        return self.colorLayers[0]    '''
        
    def getObjectColor(self):
        #self.getObjectColorLayer().getColorImg().show()
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
        print("MinMaxRange: " + str(self.getGreatestGapBetweenMaximums()))
        print("Radius: " + str(self.getMinimumBetweenMaximums(self.getGreatestGapBetweenMaximums())*self.increment))
        imgCopy = letterLayer.getColorImg()
        #Drawer.drawCircle(imgCopy, imgCopy.load(), self.cluster.getIntClusterVector(), self.getGreatestGapBetweenMaximums()[0]*self.increment, (0,255,0))
        self.croppedImg = self.getCroppedImageToRadius(self.getGreatestGapBetweenMaximums()[0]*self.increment)
        ratio = float(LetterFrames.frameHeight)/float(self.croppedImg.size[1])
        print("Ratio: " + str(ratio))
        self.croppedImg = self.croppedImg.resize((int(self.croppedImg.size[0]*ratio), int(self.croppedImg.size[1]*ratio)), PIL.Image.ANTIALIAS)
        fillRectangle = Rectangle(0, 0, 20, self.croppedImg.size[1])
        Drawer.fillRect(self.croppedImg, self.croppedImg.load(), fillRectangle, (0,0,0))
        newColorLayer = ColorLayer(self.croppedImg, self.croppedImg.load(), (255,255,255))
        newColorLayer.cropLayerToBounds()
        self.croppedImg = newColorLayer.getColorImg()
        self.croppedImg = GrayScale.getGrayScaledImage(self.croppedImg, self.croppedImg.load())
        self.croppedImg = GaussianBlur.getGaussianFilteredImage(self.croppedImg, self.croppedImg.load(), 3)
        self.sobelEdge = SobelEdge(self.croppedImg, self.croppedImg.load())
        self.sobelEdge.getSobelEdgeImg().show()
        
    def getSobelEdge(self):
        return self.sobelEdge
        
    def fillDensityFunction(self, increment):
        self.densityFunction = []
        maxRadius = sqrt((self.letterLayer.getColorImg().size[0]/2.0)**2 + (self.letterLayer.getColorImg().size[1]/2.0)**2)#temporary jank. replace with greatest possible distance from cluster point to corner of image
        
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
            
            if gap > greatestGap:
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
    
    
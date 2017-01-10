'''
Created on Jan 4, 2017

@author: phusisian
'''
from root.nested.KMeans import KMeans
from root.nested.Drawer import Drawer 
from root.nested.Rectangle import Rectangle

class LetterClusterer:
    
    def __init__(self, letterImgIn, numPoints):#even numbers tend to work better for numPoints, especially for symmetrical letters since it has an extra point on one side
        self.letterImg = letterImgIn
        self.letterImage = self.letterImg.load()
        self.dataPoints = self.toTuple()
        self.kMeans = KMeans(self.dataPoints, numPoints, 50, 1)
        '''outImg = self.getImgWithClusters()
        self.kMeans.draw(outImg, outImg.load())
        outImg.show()'''
        
    def toTuple(self):
        tuples = []
        for x in range(0, self.letterImg.size[0]):
            for y in range(0, self.letterImg.size[1]):
                if self.letterImage[x,y] != (0,0,0):
                    tuples.append((x,y))
        return tuples
    
    def getClusters(self):
        return self.kMeans.getClusters()
    
    def getImgWithClusters(self):
        img = self.letterImg.copy()
        image = img.load()
        for vector in self.kMeans.getIntClusterVectors():
            rect = Rectangle(vector[0]-2, vector[1]-2, 4, 4)
            Drawer.fillRect(img, image, rect, (0,0,255))
        return img
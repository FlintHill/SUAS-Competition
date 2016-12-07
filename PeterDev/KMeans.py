from math import sqrt
from math import pi
import random

class KMeans:
    
    def __init__(self, dataIn, numClustersIn, timesToRun, step = None):
        if step == None:
            step = timesToRun
        self.data = dataIn
        self.clusters = Clusters()
        self.timesToRun = timesToRun
        self.numClusters = numClustersIn
        self.addRandomVectorsToClusters()
        stepCount = 0
        self.fitDataToClusters(step, stepCount)
        
        for i in range(0, timesToRun):
            self.resetClustersToAverage()
            self.fitDataToClusters(step, stepCount)
            stepCount += 1
            if(step > step):
                step = 0
            
    
    @classmethod
    def initWithPicture(cls, img, image, numClusters, timesToRun, step = None):
        data = []
        for i in range(0, img.size[0]):
            for j in range(0, img.size[1]):
                data.append(image[i,j])
        KMeans.removeBlackFromData(data)
        return KMeans(data, numClusters, timesToRun, step)
    
    @staticmethod
    def removeBlackFromData(data):
        i = 0
        while i < len(data):
            if data[i] == (0,0,0):
                data.pop(i)
            else:
                i+=1
                
    def filterImageThroughClusters(self, img, image):
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                if image[x,y] != (0,0,0):#using black as a bacground, don't want picked up. Possible that a pure black will appear in real world?
                    image[x,y] = self.clusters.getSmallestDistanceCluster(image[x,y]).getIntClusterVector()
        return img
        
    def __getitem__(self, index):
        return self.data[index]
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return str(self.clusters)
        
    def getClusterVectors(self):
        vectors = []
        for i in range(0, len(self.clusters)):
            vectors.append(self.clusters[i].getClusterVector())
        return vectors
    
    def getIntClusterVectors(self):
        vectors = []
        for i in range(0, len(self.clusters)):
            vectors.append(self.clusters[i].getIntClusterVector())
        return vectors

    def addRandomVectorsToClusters(self):
        for i in range(0, self.numClusters):
            print("Len: " + str(len(self)))
            randomVector = self[int(random.random() * (len(self)-1))]
            self.clusters.append(Cluster(randomVector))#not sure if appending works with special methods
            
    def fitDataToClusters(self, step, stepCount):
        for i in range(stepCount, len(self), step):
            self.clusters.appendVectorToLeastDistanceCluster(self[i])
    
    def getClusters(self):
        return self.clusters
    
    def resetClustersToAverage(self):
        self.clusters.moveClustersToAverageAndReset()
                    
            
class Clusters:
    
    def __init__(self):
        self.clusters = []
        
    def __getitem__(self, index):
        return self.clusters[index]
    
    def __len__(self):
        return len(self.clusters)
    
    def __repr__(self):
        stringReturn = ""
        for i in range(0, len(self)):
            stringReturn += str(self[i]) + "\n "
        #stringReturn = stringReturn[0 : len(stringReturn) - 2]
        return stringReturn
    
    
    def append(self, clusterIn, name = None):
        self.clusters.append(clusterIn)
        if name != None:
            clusterIn.setName(name)
            
    
    def getSmallestDistanceCluster(self, vectorIn):
        smallestIndex = 0
        smallestDistance = self[smallestIndex].calculateDistanceFromCluster(vectorIn)
        
        for i in range(1, len(self)):
            distanceCalc = self[i].calculateDistanceFromCluster(vectorIn)
            if distanceCalc < smallestDistance:
                smallestDistance = distanceCalc
                smallestIndex = i
                
        return self[smallestIndex]

    def moveClustersToAverageAndReset(self):
        for i in range(0, len(self)):
            self[i].moveClusterToAverageAndReset()

    def appendVectorToLeastDistanceCluster(self, vectorIn):
        
        self.getSmallestDistanceCluster(vectorIn).append(vectorIn)#not sure if special methods are enough to make append work this way 

class Cluster:
    
    def __init__(self, clusterVector):
        self.clusterVector = clusterVector
        self.clusterVectors = []

    def __getitem__(self, index):
        return self.clusterVectors[index]
    
    def __len__(self):
        return len(self.clusterVectors)
    
    def __repr__(self):
        return str(self.clusterVector) + ", with average vector of: " + str(self.getAverageVector()) + ", with cluster size of: " + str(len(self))
    
    def getNumPointsInRadius(self, radius):
        count = 0
        for i in range(0, len(self)):
            if self.calculateDistanceFromCluster(self[i]) < radius:
                count += 1
        return count
    
    def getAreaOfCircle(self, radius):
        return 2*pi*(radius**2)
    
    def getDataDensityInRadius(self, radius):
        areaCircle = self.getAreaOfCircle(radius)
        if(areaCircle > 0):
            return float(self.getNumPointsInRadius(radius))/areaCircle
    
    def append(self, vectorIn):
        self.clusterVectors.append(vectorIn)
    
    def getClusterVector(self):
        return self.clusterVector
    
    def getIntClusterVector(self):#probably a better python way of doing this
        intList = []
        for i in range(0, len(self.clusterVector)):
            intList.append(int(self.clusterVector[i]))
            
        return tuple(intList)
     
    def setName(self, name):
        self.name = name   
    def getName(self):
        return self.name
    def moveClusterToAverageAndReset(self):
        self.clusterVector = self.getAverageVector()
        self.clusterVectors = []
    
    def getAverageVector(self):
        distanceAdds = [0 for i in range(0, len(self.clusterVector))]
        for i in range(len(self)):#for each vector
            for j in range(0, len(distanceAdds)):#for each dimension
                distanceAdds[j] += self[i][j]#adds to the appropriate index the vector at the dimension and index
        
        for i in range(0, len(distanceAdds)):
            if(len(self) != 0):
                distanceAdds[i] /= len(self)
            
        return tuple(distanceAdds)
    
    def appendClusterVector(self, vectorIn):#may throw error here
        self.append(vectorIn)
    
    #couldn't find an appropriate python special method to perfrom a distance calculation
    def calculateDistanceFromCluster(self, vectorIn):
        addNum = 0
        for i in range(0, len(vectorIn)):
            addNum += (vectorIn[i] - self.clusterVector[i])**2
            
        return sqrt(addNum)
    

    
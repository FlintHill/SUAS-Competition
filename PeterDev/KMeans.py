import math
from random import randint

class KMeans:
    def getKMeans(self, imgIn, numRounds, numToRun):
        #kmeans = KMeans()
        image = imgIn.load()
        dim = imgIn.size
        clusters = [0 for j in range(0,numRounds)]
        for i in range(0,numRounds):
            randX = randint(0,dim[0]-1)
            randY = randint(0,dim[1]-1)
            cluster = Cluster(image[randX, randY])
            clusters[i] = cluster
            #print(image[randX,randY])
        
        self.fitToClusters(imgIn, clusters, numRounds)
        self.resetClustersToAverage(imgIn, clusters, numRounds, 0, numToRun)
        return self.roundToClusters(imgIn, clusters)
        #return kmeans.roundToClusters(imgIn, clusters)       
        #for i in range(0, numRounds):
            #clusters[i] = Cluster(clusters[i].getAverageColor())
        
    def resetClustersToAverage(self, imgIn, clusters, numRounds, numRun, timesToRun):
        print(numRun)
        kmeans = KMeans()
        for i in range(0, numRounds):
            clusters[i] = Cluster(clusters[i].getAverageColor())
        clusters = kmeans.fitToClusters(imgIn, clusters, numRounds)
        if numRun < timesToRun:
            kmeans.resetClustersToAverage(imgIn, clusters, numRounds, numRun+1, timesToRun)
        else:
            return clusters
        
    def fitToClusters(self, imgIn, clusters, numRounds):
        image = imgIn.load()
        dim = imgIn.size
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                colorPixel = image[x,y]
                smallestDistClusterIndex = 0
                smallestDist = clusters[0].getDist(colorPixel)
                for clusterNum in range(1, numRounds):
                    if clusters[clusterNum].getDist(colorPixel) < clusters[smallestDistClusterIndex].getDist(colorPixel):
                        smallestDistClusterIndex = clusterNum
                
                clusterColor = ClusterColor(colorPixel, smallestDist)
                clusters[smallestDistClusterIndex].addColor(clusterColor)
        return clusters
        
    def roundToClusters(self, imgIn, clusters):
        image = imgIn.load()
        dim = imgIn.size
        
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                    colorPixel = image[x,y]
                    smallestDistIndex = 0
                    #smallestDist = clusters[0].getDist(colorPixel)
                    
                    for clusterNum in range(1, len(clusters)):
                        if clusters[clusterNum].getDist(colorPixel) < clusters[smallestDistIndex].getDist(colorPixel):
                            smallestDistIndex = clusterNum
                    #cColor = ClusterColor(colorPixel, smallestDist)
                    
                    image[x,y] = clusters[smallestDistIndex].getClusterColor()
        return imgIn
                    #clusters[smallestDistIndex] = cColor
                        

class Cluster:
    #colors = [0]
    def __init__(self, colorIn):
        self.color = colorIn
        self.cColors = []
    def getDist(self, colorIn):
        return math.sqrt((colorIn[0]-self.color[0])**2 + (colorIn[1]-self.color[1])**2 + (colorIn[2]-self.color[2])**2)
    
    def getClusterColor(self):
        return self.color
    
    def setClusterColor(self, colorIn):
        self.color = colorIn
        
    def addColor(self, colorIn):#takes a ClusteredColor
        self.cColors.append(colorIn)
        
    def getAverageDist(self):
        addNum = 0
        for i in range(0, len(self.cColors)):
            addNum += self.cColors[i].getDist()
        return addNum/len(self.cColors)
    
    def getAverageColor(self):
        addRed = 0
        addBlue = 0
        addGreen = 0
        for i in range(0,len(self.cColors)):
            addRed += self.cColors[i].getColor()[0]
            addGreen += self.cColors[i].getColor()[1]
            addBlue += self.cColors[i].getColor()[2]
        addRed = int(addRed/len(self.cColors))
        addGreen = int(addGreen/len(self.cColors))
        addBlue = int(addBlue/len(self.cColors))
        return (addRed,addGreen,addBlue)
        
    def printCluster(self):
        for i in range(0, len(self.cColors)):
            print("Distance")
            print(self.cColors[i].getDist())
        
class ClusterColor:
    def __init__(self, colorIn, distIn):
        self.color = colorIn
        self.dist = distIn
    def getColor(self):
        return self.color
    def getDist(self):
        return self.dist
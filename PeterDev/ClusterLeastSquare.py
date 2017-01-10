from math import atan2
from math import pi
from math import sqrt
from root.nested import KMeans
from root.nested.LetterClusterer import LetterClusterer
from root.nested.SobelEdge import SobelEdge
from root.nested.HarrisCorner import HarrisCorner
import string
from root.nested.LetterFrame import LetterFrame
from root.nested.CannyEdge import CannyEdge
from root.nested.HoughCircles import HoughCircles
import PIL
class ClusterLeastSquare:
    RADIUS_MINIMUM = 3
    '''TRY: instead of choosing a range that the num corners and num circles have to be in, instead pick a number of letters that have both the closest num corners and num circles and work off those'''
    CORNER_RANGE_RATIO = 3.0/10.0
    MIN_CORNER_RANGE = 0
    MIN_CIRCLE_RANGE = 0
    CIRCLE_RANGE_RATIO = 1.0/10.0#used to be 1.0/10.0
    def __init__(self, midpointOne, clustersOne, midpointTwo, clustersTwo):
        self.midpointOne = midpointOne
        self.midpointTwo = midpointTwo
        self.clustersOne = clustersOne
        self.clustersTwo = clustersTwo
        self.sortClusterByTheta(midpointOne, clustersOne)
        self.sortClusterByTheta(midpointTwo, clustersTwo)
      
    def getDistGrade(self):
        #errorSum = 0
        errorSquares = []
        for i in range(0, len(self.clustersOne)):
            #magDistOne = self.getDistToTupleOne(self.clustersOne[i].getIntClusterVector())
            #magDistTwo = self.getDistToTupleTwo(self.clustersTwo[i].getIntClusterVector())
            v1 = self.clustersOne[i].getIntClusterVector()
            v2 = self.clustersTwo[i].getIntClusterVector()
            distError = sqrt((v2[0] - v1[0])**2 + (v2[1] - v1[1])**2)
            errorSquares.append(distError)
                    
        #print("Error Sums: " + str(errorSquares))
        return self.sumError(errorSquares)#self.sumErrorBetweenThresholds(errorSquares, (.4, 2))#self.removeWorstFitsAndGetError(errorSquares, 2)
    
    def getAngleGrade(self):
        errorSquares = []
        for i in range(0, len(self.clustersOne)):
            #magDistOne = self.getDistToTupleOne(self.clustersOne[i].getIntClusterVector())
            #magDistTwo = self.getDistToTupleTwo(self.clustersTwo[i].getIntClusterVector())
            #if magDistOne > ClusterLeastSquare.RADIUS_MINIMUM and magDistTwo > ClusterLeastSquare.RADIUS_MINIMUM:
            angleError = (self.getAngleToCluster(self.midpointOne, self.clustersOne[i].getIntClusterVector()) - self.getAngleToCluster(self.midpointTwo, self.clustersTwo[i].getIntClusterVector()))**2
            
            errorSquares.append(angleError)
        return self.removeWorstFitsAndGetError(errorSquares, len(self.clustersOne)/4)
    
    def sumErrorBetweenThresholds(self, errorSquares, thresholds):
        errorSum = 0
        for i in range(0, len(errorSquares)):
            if errorSquares[i] > thresholds[0] and errorSquares[i] < thresholds[1]:
                errorSum += errorSquares[i]
        return errorSum
      
    def sumError(self, errorSquares):
        errorSum = 0
        for i in range(0, len(errorSquares)):
            errorSum += errorSquares[i]
        return errorSum
    
    def removeWorstFitsAndGetError(self, errorSquares, removeNum):
        #print("error squares initial: " + str(len(errorSquares)))
        for i in range(0, removeNum):
            greatestNum = errorSquares[0]
            for j in range(1, len(errorSquares)):
                if errorSquares[j] > greatestNum:
                    greatestNum = errorSquares[j]
            #print("num removed: " + str(errorSquares[errorSquares.index(greatestNum)]))
            errorSquares.pop(errorSquares.index(greatestNum))
        errorSum = 0
        #print("error squares final: " + str(len(errorSquares)))
        for i in range(0, len(errorSquares)):
            errorSum += errorSquares[i]
        return errorSum 
        
            
    def __repr__(self):
        returnString = ""
        
        for i in range(0, len(self.clustersOne)):
            returnString += "Theta One: " + str(self.getAngleToCluster(self.midpointOne, self.clustersOne[i].getIntClusterVector())) + " Theta Two: " + str(self.getAngleToCluster(self.midpointTwo, self.clustersTwo[i].getIntClusterVector())) + "\n"
            
        returnString += "Grade: " + str(self.getGrade())
        return returnString
            
    def sortClusterByTheta(self, midpoint, clusters):
        for i in range(0, len(clusters) - 1):
            lowestIndex = i
            lowestAngle = self.getAngleToCluster(midpoint, clusters[lowestIndex].getIntClusterVector())
            for j in range(i + 1, len(clusters)):
                jAngle = self.getAngleToCluster(midpoint, clusters[j].getIntClusterVector())
                if jAngle < lowestAngle:
                    lowestAngle = jAngle
                    lowestIndex = j
            
            tempPoint = clusters[i]
            clusters[i] = clusters[lowestIndex]
            clusters[lowestIndex] = tempPoint
        return None
                
    def getAngleToCluster(self, midpoint, clusterPoint):
        dx = float(clusterPoint[0]-midpoint[0])
        dy = float(clusterPoint[1]-midpoint[1])
        angle = atan2(dy, dx)
        if angle < 0:
            angle = 2.0*pi + angle
        return angle
    
    def getMaxPossibleRadiusOne(self):
        return sqrt(self.midpointOne[0]**2 + self.midpointOne[1]**2)
    
    def getMaxPossibleRadiusTwo(self):
        return sqrt(self.midpointTwo[0]**2 + self.midpointTwo[1]**2)
    
    def getDistToTupleOne(self, vector):
        return sqrt((vector[0]-self.midpointOne[0])**2 + (vector[1]-self.midpointOne[1])**2)
    
    def getDistToTupleTwo(self, vector):
        return sqrt((vector[0]-self.midpointTwo[0])**2 + (vector[1]-self.midpointTwo[1])**2)
    
class ClusterSquareFitter:
    ANGLE_WEIGHT = 0.4
    DIST_WEIGHT = 0.4
    RATIO_WEIGHT = 0.2
    defaultNumPoints = 4
    def __init__(self, letterFramesIn):
        self.letterFrames = letterFramesIn

    def getFramesWithNumCornersWithinRange(self, numCorners, rangeNum):
        cornerFrames = []
        for frame in self.letterFrames:
            if len(frame.getCorners()) >= numCorners - rangeNum and len(frame.getCorners()) <= numCorners + rangeNum:
                cornerFrames.append(frame)
        return cornerFrames 
    
    def getBestFitLetter(self, inFrames, letterImg):
        checkClusters = LetterClusterer(letterImg, ClusterSquareFitter.defaultNumPoints)
        
        
        firstFrameImg = self.cornerFrames[0].getLetterImg()
        firstFrameClusters = LetterClusterer(inFrames[0].getLetterImg(), ClusterSquareFitter.defaultNumPoints)
        firstCls = ClusterLeastSquare(self.getMidTupleFromImg(firstFrameImg), firstFrameClusters.getClusters(), self.getMidTupleFromImg(letterImg), checkClusters.getClusters())
        lowestGrade = firstCls.getGrade()
        lowestGradeIndex = 0
        for i in range(1, len(inFrames)):
            frameImg = inFrames[i].getLetterImg()
            frameClusters = LetterClusterer(frameImg, ClusterSquareFitter.defaultNumPoints)
            cls = ClusterLeastSquare(self.getMidTupleFromImg(frameImg), frameClusters.getClusters(), self.getMidTupleFromImg(letterImg), checkClusters.getClusters())
            iterGrade = cls.getGrade()
            if iterGrade < lowestGrade:
                lowestGrade = iterGrade
                lowestGradeIndex = i
                
        return inFrames[lowestGradeIndex].getLetter()  
    
    def getFramesWithNumCirclesInRange(self, inList, numCircles, rangeNum):  
        frames = []
        #print("Num Circles: " + str(numCircles))
        for i in range(0, len(inList)):
            if len(inList[i].getCircles()) >= numCircles - rangeNum and len(inList[i].getCircles()) <= numCircles + rangeNum:
                frames.append(inList[i])
        #print("Len circle frames: " + str(len(frames)))
        return frames
        ''''i = 0
        while i < len(inList):
            if not(len(inList[i].getCircles()) >= numCircles - rangeNum and len(inList[i].getCircles()) <= numCircles + rangeNum):
                inList.pop(i)
            else:
                i += 1
        return None'''
    
    def getBestFitAvgLetter(self, letterImgIn):
        
        resizeRatio = float(self.letterFrames.getFrameHeight())/float(letterImgIn.size[1])
        letterImg = letterImgIn#letterImgIn.resize((int(round(letterImgIn.size[0]*resizeRatio)), int(round(letterImgIn.size[1]*resizeRatio))), PIL.Image.BICUBIC)
        #print("Letter Img Size: " + str(letterImg.size[1]))
        #letterImg.show()
        checkClusters = LetterClusterer(letterImg, ClusterSquareFitter.defaultNumPoints)
        distGrades = []
        angleGrades = []
        ratioGrades = []
        letterList = dict(enumerate(string.ascii_uppercase, 0))
        cannyImg = CannyEdge.getCannyEdgeImage(SobelEdge(letterImg, letterImg.load()), 40, 10)
        numCircles = len(HoughCircles(cannyImg, cannyImg.load(), LetterFrame.RADIUS_BOUNDS).getCirclesOverThreshold(LetterFrame.CIRCLE_THRESHOLD))
        print("num circles: " + str(numCircles) )
        numCorners = len(HarrisCorner.getCorners(letterImg, letterImg.load(), SobelEdge(letterImg, letterImg.load()), LetterFrame.HARRIS_KERNELSIZE, LetterFrame.HARRIS_STDDEV, LetterFrame.HARRIS_THRESHOLD))
        #height of image * imgRatio = width of image
        imgRatio = float(letterImg.size[0])/float(letterImg.size[1])
        cornerFrames = self.getFramesWithNumCornersWithinRange(numCorners, ClusterLeastSquare.MIN_CORNER_RANGE + int(ClusterLeastSquare.CORNER_RANGE_RATIO * float(numCorners)) + 1)
        #self.removeFramesWithCirclesOutsideOfRange(cornerFrames, numCircles, 4)
        cornerFrames = self.getFramesWithNumCirclesInRange(cornerFrames, numCircles, ClusterLeastSquare.MIN_CIRCLE_RANGE + (numCircles * ClusterLeastSquare.CIRCLE_RANGE_RATIO))
        #print("Corner Frames Size: " + str(len(cornerFrames)))
        
        for i in range(0, len(cornerFrames)):
            frameImg = cornerFrames[i].getLetterImg()
            frameClusters = LetterClusterer(frameImg, ClusterSquareFitter.defaultNumPoints)
            cls = ClusterLeastSquare(self.getMidTupleFromImg(frameImg), frameClusters.getClusters(), self.getMidTupleFromImg(letterImg), checkClusters.getClusters())
            
            
            
            distGrades.append((cornerFrames[i].getLetter(), cls.getDistGrade())) 
            angleGrades.append((cornerFrames[i].getLetter(), cls.getAngleGrade()))
            
            widthOfFrameIfUsedLetterRatio = cornerFrames[i].getLetterImg().size[1]*imgRatio
            widthDistOff = abs(cornerFrames[i].getLetterImg().size[0] - widthOfFrameIfUsedLetterRatio)
            ratioGrades.append((cornerFrames[i].getLetter(), widthDistOff))
            
            
        #print("dist grades size: " + str(len(distGrades)))
        
        return self.findBestAverageWeightedPlaceScore(distGrades, angleGrades, ratioGrades)
    
    '''def findBestAverageWeightedPlaceScore(self, distGrades, angleGrades):
        self.sortScores(distGrades)
        self.sortScores(angleGrades)
        print("dist grades: " + str(distGrades))
        print("angle grades: " + str(angleGrades))
        ties = []
        lowestAvgScore = self.getAvgWeightedPlacementScoreOfLetter(distGrades[0][0], distGrades, angleGrades)
        lowestAvgScoreLetter = distGrades[0][0]
        lowestScoreIndex = 0
        for i in range(1, len(distGrades)):
            iterScore = self.getAvgWeightedPlacementScoreOfLetter(distGrades[i][0], distGrades, angleGrades)
            
            if iterScore < lowestAvgScore:
                lowestAvgScore = iterScore
                lowestScoreIndex = i
                lowestAvgScoreLetter = distGrades[i][0]
        return lowestAvgScoreLetter
        '''
        
    def findBestAverageWeightedPlaceScore(self, distGrades, angleGrades, ratioGrades):
        self.sortScores(distGrades)
        self.sortScores(angleGrades)
        self.sortScores(ratioGrades)#RATIO GRADES CAN OFTEN TIE, AND WEIGHTING TIED GRADES CAN GIVE UNFAIR LOWER WEIGHT TO LETTERS OF EQUAL RATIO. ACCOUNT FOR TIES.
        print("dist grades: " + str(distGrades))
        print("angle grades: " + str(angleGrades))
        print("ratio grades: " + str(ratioGrades))
        averageScores = self.getAverageScores(distGrades, angleGrades, ratioGrades)
        self.sortScores(averageScores)
        return averageScores[0][0]
        
    def getAverageScores(self, distGrades, angleGrades, ratioGrades):
        weightedGrades = []
        for i in range(0, len(distGrades)):
            iterLetter = distGrades[i][0]
            distIndex = i
            angleIndex = self.getIndexOfLetterInList(angleGrades, iterLetter)
            ratioIndex = self.getIndexOfLetterInList(ratioGrades, iterLetter)
            weightedGrade = ((ClusterSquareFitter.ANGLE_WEIGHT * angleIndex + ClusterSquareFitter.DIST_WEIGHT * distIndex + ClusterSquareFitter.RATIO_WEIGHT * ratioIndex)+1)/(ClusterSquareFitter.ANGLE_WEIGHT + ClusterSquareFitter.DIST_WEIGHT + ClusterSquareFitter.RATIO_WEIGHT)
            weightedGrades.append((iterLetter, weightedGrade))
        return weightedGrades
    
    def getIndexOfLetterInList(self, listIn, letter):
        for i in range(0, len(listIn)):
            if listIn[i][0] == letter:
                return i
            
        return None
    
    def sortScores(self, scores):
        for i in range(0, len(scores)-1):
            lowestScoreIndex = i
            for j in range(i+1, len(scores)):
                if scores[j][1] < scores[lowestScoreIndex][1]:
                    lowestScoreIndex = j
            
            temp = scores[i]
            scores[i] = scores[lowestScoreIndex]
            scores[lowestScoreIndex] = temp
            
    def getAvgWeightedPlacementScoreOfLetter(self, letter, distGrades, angleGrades):
        distIndex = 0
        angleIndex = 0
        for i in range(0, len(distGrades)):
            if distGrades[i][0] == letter:
                distIndex = i
            if angleGrades[i][0] == letter:
                angleIndex = i
        return (float(float(distIndex * ClusterSquareFitter.DIST_WEIGHT) + float(angleIndex * ClusterSquareFitter.ANGLE_WEIGHT)))/float(ClusterSquareFitter.ANGLE_WEIGHT + ClusterSquareFitter.DIST_WEIGHT)
        #return (distScore, angleScore)
    
    def getMidTupleFromImg(self, img):
        return (img.size[0]/2, img.size[1]/2)
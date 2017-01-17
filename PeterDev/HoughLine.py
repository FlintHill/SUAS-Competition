'''
Created on Jan 11, 2017

@author: phusisian
'''
from math import sqrt
from math import pi
from math import sin
from math import cos
from root.nested.Rectangle import Rectangle
from root.nested.Drawer import Drawer
class HoughLine:
    
    '''need to find a good way to account for inaccuracies so I can lower step values'''
    RADIUS_STEP = 1
    '''will need to mess with THETA_STEP like I did with Hough circles so it only 
    steps as much as it has to.'''
    THETA_STEP = pi/128.0
    THETA_LEN = int(2.0*pi/THETA_STEP)
    #STEP_MULTIPLIER = 4.0
    ''' is the minimum gap that would allow two slightly different 
    thetas to be possibly in the same line, to account for error'''
    THETA_GAP = pi#6.0*(pi/32.0) 
    
    def __init__(self, cannyImg, cannyImage):
        self.cannyImg = cannyImg
        self.cannyImage = cannyImage
        self.maxRadius = self.getMaxRadius()
        self.centerPoint = (cannyImg.size[0]/2, cannyImg.size[1]/2)
        self.setAccumulatorMatrix()
        
    def setAccumulatorMatrix(self):
        self.accumulator = [RadiusThetaHolder(int(i*HoughLine.RADIUS_STEP)) for i in range(-int(self.maxRadius) - 1, int(self.maxRadius) + 1, HoughLine.RADIUS_STEP)]
        for x in range(-self.centerPoint[0], self.centerPoint[0]):
            for y in range(-self.centerPoint[1], self.centerPoint[1]):
                if not self.cannyImage[self.centerPoint[0] + x, self.centerPoint[1] + y] == (0,0,0) and not self.cannyImage[self.centerPoint[0] + x, self.centerPoint[1] + y] == (0,0,0,0):
                    theta = 0
                    #print("XY: " + str(x) + ", " + str(y))
                    while theta < pi*2.0:
                        r = int(x*cos(theta) + y*sin(theta))
                        '''print("max radius: " + str(self.maxRadius))
                        print("r: " + str(r))'''
                        self.getRadiusThetaHolderOfRadius(r).voteForTheta(theta)
                        theta += HoughLine.THETA_STEP
    
    
    def getLinesOverThreshold(self, threshold):
        lines = []
        for i in range(0, len(self.accumulator)):
            iterHighestVoteAndTheta = self.accumulator[i].getHighestVoteAndTheta()
            if iterHighestVoteAndTheta[1] >= threshold:
                xBase = int(self.centerPoint[0] + self.accumulator[i].getRadius() * cos(iterHighestVoteAndTheta[0]))
                yBase = int(self.centerPoint[1] + self.accumulator[i].getRadius() * sin(iterHighestVoteAndTheta[0]))
                thetaLine = ThetaLine(iterHighestVoteAndTheta, (xBase, yBase), iterHighestVoteAndTheta[0] + (pi/2.0))
                lines.append(thetaLine)
        return self.getRealLines(lines)
    
    def drawLinesOverThreshold(self, img, image, threshold, color):
        thresholdLines = self.getLinesOverThreshold(threshold)
        print("threshold lines size: " + str(len(thresholdLines)))
        for i in range(0, len(thresholdLines)):
            thresholdLines[i].draw(img, image, color)
        return img
    
    def getRadiusThetaHolderOfRadius(self, radius):
        halfRadiusStep = HoughLine.RADIUS_STEP/2.0
        for i in range(0, len(self.accumulator)):
            if radius >= self.accumulator[i].getRadius() - halfRadiusStep and radius <= self.accumulator[i].getRadius() + halfRadiusStep:
                return self.accumulator[i]
        
    def getMaxRadius(self):
        return sqrt((self.cannyImg.size[0]/2)**2 + (self.cannyImg.size[1]/2)**2)
    
    def getRealLines(self, lines):
        realLines = []
        #i = 0
        while len(lines) > 0:
        #while i < len(lines):
            #thetaLines = self.getLinesWithThetaInRange(lines[0].getVoteAndTheta()[0], lines, HoughLine.THETA_GAP)
            thetaLines = self.getLinesSortedByVote(lines)
            realAddLines = self.getLinesWithinRadiusRange(thetaLines, ThetaLine.MIN_RADIUS_APART)
            self.removeLinesFromLines(lines, thetaLines)
            self.addLinesToLines(realLines, realAddLines)
        return realLines
         
    '''takes lines sorted by vote'''
    def getLinesWithinRadiusRange(self, lines, radiusRange):
        radiusLines = []
        #print("radius lines in: " + str(len(lines)))
        for i in range(0, len(lines)):
            if self.lineOutsideOfRadiusRange(lines[i], radiusLines, radiusRange):
                radiusLines.append(lines[i])
        #print("radius lines out: " + str(len(radiusLines)))
        return radiusLines

    
    def removeLinesFromLines(self, baseLines, removeLines):
        for i in range(0, len(removeLines)):
            removeIndex = baseLines.index(removeLines[i])
            baseLines.pop(removeIndex)
        return None
        
    def addLinesToLines(self, baseLines, addLines):
        for i in range(0, len(addLines)):
            baseLines.append(addLines[i])
        return None
    '''
    def getLinesWithThetaInRange(self, theta, lines, thetaRange):
        thetaLines = []
        for i in range(0, len(lines)):
            if lines[i].getVoteAndTheta()[0] >= theta - thetaRange and lines[i].getVoteAndTheta()[0] <= theta + thetaRange:
                print("Theta in: "  + str(theta) + " theta range: " + str(thetaRange) + " vote and theta: " + str(lines[i].getVoteAndTheta()))

                thetaLines.append(lines[i])
        return thetaLines
    '''
    def getLinesSortedByVote(self, lines):
        print("lines size: " + str(len(lines)))
        print(sorted(lines, key=lambda line: -line.getVoteAndTheta()[1]))
        return sorted(lines, key=lambda line: -line.getVoteAndTheta()[1])
    
    def lineOutsideOfRadiusRange(self, line, lines, radiusRange):
        for i in range(0, len(lines)):
            if lines[i].getBaseDistanceToLine(line) < radiusRange:
                return False
        return True
        
    def __repr__(self):
        outString = ""
        for i in range(0, len(self.accumulator)):
            outString += str(self.accumulator[i]) + "\n"
        return outString
    
class RadiusThetaHolder:
    def __init__(self, radius):
        self.radius = radius
        self.thetaVotes = [0 for i in range(0, HoughLine.THETA_LEN)]
        
    def voteForTheta(self, theta):
        self.thetaVotes[self.getIndexOfTheta(theta)] += 1
        
    def getIndexOfTheta(self, theta):
        return int(theta/HoughLine.THETA_STEP)
    
    def convertIndexToTheta(self, index):
        return index * HoughLine.THETA_STEP
    
    def getRadius(self):
        return self.radius
    
    def getHighestVoteAndTheta(self):
        highestVoteIndex = 0
        for i in range(1, len(self.thetaVotes)):
            if self.thetaVotes[i] > self.thetaVotes[highestVoteIndex]:
                highestVoteIndex = i
        return(self.convertIndexToTheta(highestVoteIndex)%(2.0*pi), self.thetaVotes[highestVoteIndex])        
     
    def __repr__(self):
        return "Radius: " + str(self.radius) + ", " + str(self.getHighestVoteAndTheta())
            

class ThetaLine:
    '''MIN_RADIUS_APART needs to be dependent upon the dimensions of the image'''
    MIN_RADIUS_APART = 20.0
    '''little clunky that there are redundant, equal copies of class information helf both in voteAndTheta and class variables'''
    #to get rid of extra lines, try to look for ones within a radius and angle, then choose the one with the highest vote
    def __init__(self, voteAndTheta, base, angle):
        self.voteAndTheta = voteAndTheta
        self.base = base
        self.angle = angle%(2.0*pi)
    
    def __repr__(self):
        outString = "Line with vote: " + str(self.voteAndTheta[1]) + " with base: " + str(self.base) + " with angle: " + str(self.angle)
        return outString
    
    def getAngle(self):
        return self.angle
    
    def getParX(self, t):
        return self.base[0] + cos(self.angle)*t
    
    def getParY(self, t):
        return self.base[1] + sin(self.angle)*t

    def getVoteAndTheta(self):
        return self.voteAndTheta

    def draw(self, img, image, color):
        for t in range(-50, 50):
            xCoord = int(self.getParX(t))
            yCoord = int(self.getParY(t))
            if xCoord > 0 and xCoord < img.size[0] and yCoord > 0 and yCoord < img.size[1]:
                image[xCoord, yCoord] = color
        baseRect = Rectangle(self.base[0]-10, self.base[1]-10, 20, 20)
        Drawer.fillRect(img, image, baseRect, (0,0,255))
        return img
    
    def getBase(self):
        return self.base
    
    def getBaseDistanceToLine(self, checkLine):
        return sqrt((checkLine.getBase()[0] - self.base[0])**2  +  (checkLine.getBase()[1] - self.base[1])**2)
    

    '''
    def setAccumulatorMatrix(self):
        self.maxRadius = self.getMaxRadiusOfImg()
        maxRadius = self.maxRadius
        radiusLength = int(maxRadius/HoughLine.RADIUS_STEP)
        thetaLength = HoughLine.THETA_LEN
        #radius is x, theta is y
        self.accumulator = [[0 for j in range(0, thetaLength)] for i in range(0, radiusLength)]
        center = (self.cannyImg.size[0]/2, self.cannyImg.size[1]/2)
        self.center = center
        for x in range(0, self.cannyImg.size[0]):
            for y in range(0, self.cannyImg.size[1]):
                if self.cannyImage[x,y] != (0,0,0) and self.cannyImage[x,y] != (0,0,0,0):
                    self.setPointVotes((x,y), center)
                    
        print(self.accumulator)
        
    def drawHighestWeightPosition(self, img, image):
        highestWeight = self.accumulator[0][0]
        highestIndexes = (0,0)
        for i in range(1, len(self.accumulator)):
            for j in range(1, len(self.accumulator[0])):  
                if self.accumulator[i][j] > highestWeight:
                    highestWeight = self.accumulator[i][j]    
                    highestIndexes = (i,j)
        vals = self.convertAccumulatorIndexesToValues(highestIndexes)
        print("vals: " + str(vals))
        pLine = PolarLine((vals[0]*cos(vals[1]), vals[0]*sin(vals[1])), vals[1] + (pi/2.0))
        pLine.draw(self.center, img, image)
        img.show()
        
    def drawLinesOverThreshold(self, img, image, threshold):
        vals = self.getValuesOverThreshold(threshold)
        for i in range(0, len(vals)):
            pLine = PolarLine((vals[i][0] * cos(vals[i][1]), vals[i][0] * sin(vals[i][1])), vals[i][1]+(pi/2.0))
            pLine2 = PolarLine((vals[i][0] * cos(vals[i][1]), vals[i][0] * sin(vals[i][1])), vals[i][1])
            pLine.draw(img, image, (255,0,0))
            pLine2.draw(img, image, (0,0,255))
        img.show()
        return img    
        
    def getValuesOverThreshold(self, threshold):
        indexes = []
        for x in range(0, len(self.accumulator)):
            for y in range(0, len(self.accumulator[0])):
                if self.accumulator[x][y] > threshold:
                    indexes.append(self.convertAccumulatorIndexesToValues((x,y)))
        return indexes
        
    def convertAccumulatorIndexesToValues(self, point):
        return (point[0]*HoughLine.RADIUS_STEP, point[1]*HoughLine.THETA_STEP) 
                    
    def setPointVotes(self, pixelPoint, center):
        for thetaIndex in range(0, HoughLine.THETA_LEN):
            theta = thetaIndex * HoughLine.THETA_STEP
            
            r = int((pixelPoint[0]-center[0])*cos(theta) + (pixelPoint[1]-center[1])*sin(theta))
            self.accumulator[r][thetaIndex] += 1#may out of bounds here?
            
        
    
    
    def getMaxRadiusOfImg(self):
        return sqrt((self.cannyImg.size[0]/2)**2 + (self.cannyImg.size[1]/2)**2)
    
class PolarLine:
    def __init__(self, base, angle):
        self.base = base
        self.angle = angle
    
    def getParX(self, t):
        return self.base[0] + cos(self.angle)*t
    
    def getParY(self, t):
        return self.base[1] + sin(self.angle)*t
    
    def draw(self, img, image, color):
        for t in range(-50, 50):
            try:
                image[int((img.size[0]/2) + self.getParX(t)), int((img.size[1]/2)+self.getParY(t))] = color
            except:
                print("hi")
        return img'''
        
from imageop.Point import Point
from imageop.Line import Line
from imageop.Rectangle import Rectangle
from PIL import Image

class Polygon:
    defaultMaskMargin = 1
    def __init__(self, pointsIn):
        self.points = pointsIn
        self.setLines()
    
    '''sets the lines that make up the polygon. Note this may need to be called again if the polygon is scaled, translated, moved...
    unless Python uses pointers to points that this takes, in which case, I *think* that this wouldn't need to be recalled in those
    instances'''
    def setLines(self):
        self.lines = []
        for i in range(0, len(self.points)):
            if i < len(self.points) - 1:
                appendLine = Line(self.points[i], self.points[i+1])
                self.lines.append(appendLine)
            else:
                appendLine = Line(self.points[i], self.points[0])
                self.lines.append(appendLine)
    
    def draw(self, image, color):
        for i in range(0, len(self.lines)):
            self.lines[i].draw(image, color)
    
    '''draws the polygon after it has been translated using translated point's x and y as dx and dy'''
    def drawTranslated(self, image, color, translatedPoint):
        for i in range(0, len(self.lines)):
            self.lines[i].drawTranslatedLine(image, color, translatedPoint)
    
    def fill(self, img, image, color):
        marginBounds = self.getBoundsWithMargin(Polygon.defaultMaskMargin)
        maskImg = self.getFilledMask(marginBounds, color)
        self.pasteMaskToBase(marginBounds, img, maskImg)
        return None
      
    '''fill with the given color, and apply the grayGradientMaker's gradient to the filled polygon'''  
    def fillWithGradient(self, img, image, color, grayGradientMaker):
        marginBounds = self.getBoundsWithMargin(Polygon.defaultMaskMargin)
        maskImg = self.getGradientFilledMask(marginBounds, color, grayGradientMaker)
        maskImage = maskImg.load()
        self.pasteMaskToBase(marginBounds, img, maskImg)#make sure the mask being applied is a HEALTHY margin bigger than the bounding box of the polygon's mask
        return None
    
    def pasteMaskToBase(self, marginBounds, img, maskImg):  
        img.paste(maskImg, (marginBounds.getX(), marginBounds.getY()), maskImg.convert('RGBA'))#possible there is a one-pixel off when pasted
        return None
            
    def getFilledMask(self, marginBounds, color):
        maskImg = Image.new('RGBA', (marginBounds.getWidth(), marginBounds.getHeight()))
        maskImage = maskImg.load()
        self.drawTranslated(maskImage, color, Point(-marginBounds.getX(), -marginBounds.getY() ))#may throw error here since 1 or something needs to be added
        for y in range(0, marginBounds.getHeight()):
            intersections = self.getIntersectionsAtYUsingMask(maskImage, y, marginBounds, color)
            fillLines = self.getFillLines(intersections)
            for line in fillLines:
                line.draw(maskImage, color)
        return maskImg
       
    def getGradientFilledMask(self, marginBounds, color, grayGradientMaker):
        maskImg = self.getFilledMask(marginBounds, color)
        grayGradientMaker.applyGradients(maskImg, maskImg.load())
        return maskImg
     
    '''gets the number of intersections that a scanline at y will ahve with the polygon drawn into the mask.
    used for scanline polygon filling. clunky name.''' 
    def getIntersectionsAtYUsingMask(self, image, yIn, bounds, color):
        intersections = []
        for x in range(0, bounds.getWidth()):
            if image[x,yIn][3] != 0 and image[x-1, yIn][3] == 0:
                intersections.append(Point(x, yIn))
        return intersections
    
    def getBounds(self):
        highestPoint = self.getHighestPoint()
        lowestPoint = self.getLowestPoint()
        leftestPoint = self.getLeftestPoint()
        rightestPoint = self.getRightestPoint()
        return Rectangle(leftestPoint.getX(), highestPoint.getY(), rightestPoint.getX() - leftestPoint.getX(), lowestPoint.getY() - highestPoint.getY())
    
    def getBoundsWithMargin(self, margin):
        bounds = self.getBounds()
        return Rectangle(bounds.getX() - margin, bounds.getY() - margin, bounds.getWidth() + margin*2 + 1, bounds.getHeight() + margin*2 + 1)
    
    '''polygon loses all points except those that are within the crop rectangle. (this can be used to get quartercircles and semicricles)'''
    def crop(self, cropRect):
        cropPoints = []
        for i in range(0, len(self.points)):
            if cropRect.contains(self.points[i]):
                cropPoints.append(self.points[i])
        self.points = cropPoints
        self.setLines()
    
    '''SETS (is incosistent with point, which returns something) this polygon instance to use only integers for its points'''
    def toInt(self):
        for i in range(0, len(self.points)):
            self.points[i] = self.points[i].toInt()
        self.setLines()
        return None
    
    def getPoints(self):
        return self.points
    
    def insert(self, index, point):
        self.points.insert(index, point)
    
    def rotate(self, pivot, rotation):
        for i in range(0, len(self.points)):
            self.points[i].rotate(pivot, rotation)
        self.setLines()
        return None
    
    def getMidpoint(self):
        xAdd = 0
        yAdd = 0
        for i in range(0, len(self.points)):
            xAdd += self.points[i].getX()
            yAdd += self.points[i].getY()
        xAdd = float(xAdd)/float(len(self.points))
        yAdd = float(yAdd)/float(len(self.points))
        return Point(xAdd, yAdd)
    
    '''not really sure if this works/is useful. Was a potential solution to a certain issue, but ended up not being used. Returns the
    location of the midpoint relative to the bounds of the polygon'''
    def getMidpointWithinBounds(self):
        outOfBoundsMidpoint = self.getMidpoint()
        bounds = self.getBounds()
        return Point(outOfBoundsMidpoint.getX() - bounds.getX(), outOfBoundsMidpoint.getY() - bounds.getY())
    
    def getFillLines(self, intersectPoints):
        fillLines = []
        for i in range(0, len(intersectPoints) - 1, 2):
            addLine = Line(intersectPoints[i], intersectPoints[i+1])
            fillLines.append(addLine)
        return fillLines
    
    '''All the below are for simple bounding operations'''    
    def getHighestPoint(self): 
        highestIndex = 0
        for i in range(1, len(self.points)):
            if self.points[i].getY() < self.points[highestIndex].getY():
                highestIndex = i
        return self.points[highestIndex]
    def getLeftestPoint(self):
        leftestIndex = 0
        for i in range(1, len(self.points)):
            if self.points[i].getX() < self.points[leftestIndex].getX():
                leftestIndex = i
        return self.points[leftestIndex]
    def getRightestPoint(self):
        rightestIndex = 0
        for i in range(1, len(self.points)):
            if self.points[i].getX() > self.points[rightestIndex].getX():
                rightestIndex = i
        return self.points[rightestIndex]
    def getLowestPoint(self): 
        lowestIndex = 0
        for i in range(1, len(self.points)):
            if self.points[i].getY() > self.points[lowestIndex].getY():
                lowestIndex = i
        return self.points[lowestIndex]
              
    
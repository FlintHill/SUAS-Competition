from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
import EdgeDetection
import Point
import Line

class LineCaster:
    
    def __init__(self, imgIn):
        self.letterImg = imgIn
        self.increment = (25.0/500.0)*(self.letterImg.size[1]/0.668)#increments a different amount based on the height of the image (clunky math here because it was made to be used with a font size and I instead switched it to use the height of the image)
        
        self.setWireFrame()
        self.setLetterPoints()
        self.setLetterLines()
        
    
    def setLetterLines(self):
        lines = []#may want to make a 2d array
        draw = ImageDraw.Draw(self.letterImg)
        '''for y in range(0, len(self.letterPoints[0])):
            for x in range(0, len(self.letterPoints)):
                lines.append(Line.Line(self.letterPoints[x][y], self.letterPoints[x][y+4]))'''
        highestNumPoints = 0
        y = 0
        while y < (float(self.letterImg.size[1])/self.increment) - 1:
        #for y in range(0, (float(self.letterImg.size[1])/self.increment) - 1):
            if self.getNumPointsAtHeight(y) > highestNumPoints:
                highestNumPoints = self.getNumPointsAtHeight(y)
            y += 1
        y=0
        while y < (float(self.letterImg.size[1])/self.increment) - 1:
        #for y in range(0, (float(self.letterImg.size[1])/self.increment) - 1):
            for x in range(0, len(self.getPointsAtHeight(y))):
                if len(self.getPointsAtHeight(y)) == highestNumPoints and len(self.getPointsAtHeight(y+1)) == highestNumPoints:
                    try:
                        draw.fontmode = "1"
                        draw.text((self.getPointsAtHeight(y)[x].getX() , self.getPointsAtHeight(y)[x].getY()), str(x) + ", " + str(y), (0,255,0), font = ImageFont.truetype("Amble-Regular.ttf", 20))
                        lines.append(Line.Line(self.getPointsAtHeight(y)[x], self.getPointsAtHeight(y+1)[x]))
                    except:
                        print("hi")
            y+=1
        self.letterLines = lines
        for i in range(0, len(lines)):
            lines[i].drawLine(self.letterImg, (0,0,255))
        self.letterImg.show()
        
        
    def getNumPointsAtHeight(self, indexHeight):
        count = 0
        for i in range(0, len(self.letterPoints)):
            if self.letterPoints[i].getY()/self.increment == indexHeight:
                count += 1
                
        return count
    
    def getPointsAtHeight(self, indexHeight):
        gR = []
        for i in range(0, len(self.letterPoints)):
            if self.letterPoints[i].getY()/self.increment == indexHeight:
                gR.append(self.letterPoints[i])
                
        return gR
    

    def setWireFrame(self):
        image = self.letterImg.load()
        dim = self.letterImg.size
        
        edges = EdgeDetection.EdgeDetection().getLetterEdges(self.letterImg)
        giveReturn = [[False for i in range(0, dim[1])] for j in range(0, dim[0])]
        for y in range(0, dim[1]):
            edgeFound = False
            edgePoints = []
            for x in range(0, dim[0]):
                
                if edgeFound == False and image[x,y] == (255,255,255):
                    edgePoints.append(Point.Point(x, y))
                    edgeFound = True
                elif edgeFound == True and image[x,y] != (255,255,255):
                    edgePoints.append(Point.Point(x,y))
                    edgeFound = False
                if len(edgePoints) > 1:
                    giveReturn[edgePoints[0].getX() + ((edgePoints[1].getX() - edgePoints[0].getX())/2)][y] = True
                    edgePoints = []
       
        self.wireFrame = giveReturn
      
    def setLetterPoints(self):
        
        image = self.letterImg.load()
        
        dim = self.letterImg.size
        unsortedPoints = []#POINTS GOES Y,X
        y = 0
        greatestPointsAtRow = 0
        while y < dim[1]:
            pointsAtRow = 0
            for x in range(0, dim[0]):
                if self.wireFrame[x][int(y)] == True:
                    pointsAtRow+=1
                    unsortedPoints.append(Point.Point(x,y))
            if greatestPointsAtRow < pointsAtRow:
                greatestPointsAtRow = pointsAtRow
            elif pointsAtRow < greatestPointsAtRow:
                for i in range(0, greatestPointsAtRow-pointsAtRow):
                    unsortedPoints.append(unsortedPoints[len(unsortedPoints)-1])
            y+=self.increment
            
        draw = ImageDraw.Draw(self.letterImg)
        
        self.letterPoints = unsortedPoints
        self.letterImg.show()
    
    
    def getLines(self):
        return self.letterLines
        
    def getSlopeImage(self):
        imgR = Image.new("RGB", (1000,1000))
        for i in range(0, len(self.letterLines)):
            self.letterLines[i].drawLine(imgR,(255,0,0))
        return imgR
      
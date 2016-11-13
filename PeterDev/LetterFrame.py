'''
Created on Nov 4, 2016

@author: phusisian
'''

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import EdgeDetection
import ObjectDetection
import Paint
import Point
import Line
from __builtin__ import True
import math
#img = Image.open("sample_in.jpg")
#draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
#>>> font = ImageFont.truetype("sans-serif.ttf", 16)
# draw.text((x, y),"Sample Text",(r,g,b))
#>>> draw.text((0, 0),"Sample Text",(255,255,255),font=font)
#>>> img.save('sample-out.jpg')

class LetterFrame:
    
    def __init__(self, letterIn, fontIn, sizeIn): #Problem: lower-case g gets cut off (and q, p as well I assume) since the tail goes underneath the image
        
        self.font = ImageFont.truetype(fontIn, sizeIn)
        self.size = sizeIn
        
        if letterIn != None:
            self.letter = letterIn
            self.setLetterImage()
        self.increment = (25.0/500.0)*(self.letterImg.size[1]/0.668)#(25.0/500.0)*self.size
        self.setFrame()#Problem: setFrame is called twice because you need the edges to crop the image, but then the edges aren't cropped so it is done again with the cropped iamge
        self.cropImage()
        self.setWireFrame()
        self.setLetterPoints()
        self.setLetterLines()
        self.cropImage()
        
    def getLeastSlopeSquare(self, lines):
        count = 0
        for i in range(0, len(lines)):
            if abs(len(lines) - len(self.letterLines)) >= 2:
                return 100 #arbitrarily large number
            try:
                count += (math.atan2(lines[i].getdy(), lines[i].getdx()) - math.atan2(self.letterLines[i].getdy(),self.letterLines[i].getdx()))**2
            except:
                print("line index out of bounds")
        return count
        
    def getLines(self):
        return self.letterLines
        
    def setLetterImage(self):
        self.letterImg = Image.new("RGB", (self.size*3,self.size*3))
        draw = ImageDraw.Draw(self.letterImg)
        draw.fontmode = "1"
        draw.text((1,1), self.letter, (255,255,255), font = self.font)
        
    def setFrame(self):
        #ed = EdgeDetection.EdgeDetection()
        #self.letterFrame = ed.getKMeansEdges(self.letterImg)
        #print(len(self.letterFrame))
        #print(len(self.letterFrame[0]))
        image = self.letterImg.load()
        dim = self.letterImg.size
        edges = [[False for i in range(dim[1])] for j in range(dim[0])]
        for x in range(1, dim[0]):
            for y in range(1, dim[1]):
                if image[x,y] == (255,255,255):
                    edges[x][y] = True
        self.letterFrame = edges
    
    def setLetterPoints(self):
        
        image = self.letterImg.load()
        
        dim = self.letterImg.size
        unsortedPoints = []#POINTS GOES Y,X
        y = 0
        greatestPointsAtRow = 0
        while y < dim[1]:
        #for y in range(0, dim[1], self.increment):
            pointsAtRow = 0
            for x in range(0, dim[0]):
                if self.wireFrame[x][int(y)] == True:
                    #points[y%increment].append(Point.Point(x,y))
                    pointsAtRow+=1
                    unsortedPoints.append(Point.Point(x,y))
                    #points[int(y/increment)].append(Point.Point(x,y))
                    #image[x,y] = (255,0,0)
            if greatestPointsAtRow < pointsAtRow:
                greatestPointsAtRow = pointsAtRow
            elif pointsAtRow < greatestPointsAtRow:
                for i in range(0, greatestPointsAtRow-pointsAtRow):
                    unsortedPoints.append(unsortedPoints[len(unsortedPoints)-1])
            y+=self.increment
                
            
            #for i in range(0, len(linePoints)):
                #points[i][y%increment] = linePoints[i]
            
        draw = ImageDraw.Draw(self.letterImg)
        
        '''for i in range(0, len(points)):
            for j in range(0, len(points[0])):
                
                image[points[i][j].getX(), points[i][j].getY()] = (255,0,0)
                draw.fontmode = "1"
                draw.text((points[i][j].getX() , points[i][j].getY()), str(i) + ", " + str(j), (0,255,0), font = ImageFont.truetype("Amble-Regular.ttf", 20))
                '''
        self.letterPoints = unsortedPoints
        #self.letterImg.show()
    
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
                        #draw.text((self.getPointsAtHeight(y)[x].getX() , self.getPointsAtHeight(y)[x].getY()), str(x) + ", " + str(y), (0,255,0), font = ImageFont.truetype("Amble-Regular.ttf", 20))
                        lines.append(Line.Line(self.getPointsAtHeight(y)[x], self.getPointsAtHeight(y+1)[x]))
                    except:
                        print("hi")
            y+=1
        self.letterLines = lines
        #for i in range(0, len(lines)):
            #lines[i].drawLine(self.letterImg, (0,0,255))
        #self.letterImg.show()
    
    def setWireFrame(self):
        image = self.letterImg.load()
        dim = self.letterImg.size
        #edgePoints = []
        '''
        edges = EdgeDetection.EdgeDetection().getLetterEdges(self.letterImg)
        for y in range(0, dim[1]):
            edgePoints = EdgeDetection.EdgeDetection().getEdgesAtRow(edges, y)
            for x in range(0, dim[0]):
                if len(edgePoints) > 1:
                    if x > edgePoints[0].getX() and x < edgePoints[len(edgePoints)-1].getX() and image[x,y] != (255,255,255):
                        image[x,y] = (255,255,255)
        '''
        
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
                    #if edges[x][y] == True and edgeFound == False:
                        
        #edges = [[False for i in range(dim[1])] for j in range(dim[0])]
        #edges = [[False for i in range(dim[1])] for j in range(dim[0])]
        #edges = EdgeDetection.EdgeDetection().getLetterEdges(self.letterImg)
       
        self.wireFrame = giveReturn
      
    def cropImage(self):
        objDetect = ObjectDetection.ObjectDetection()
        clip = objDetect.getLayerBounds(self.letterFrame, True)
        
        #paint = Paint.Paint()
        #self.letterImg = paint.drawRectangle(self.letterImg, clip, (0,255,0))#
        self.letterImg = self.letterImg.crop((clip.getX() - 1, clip.getY()-1, clip.getX() + clip.getWidth()+2, clip.getY() + clip.getHeight()+2))
        #self.letterImg.show()
        #print("Letter size: {}".format(self.letterImg.size[1]))
        #print(self.letterImg.size[0])
        self.letterFrame = [[False for i in range(0, self.letterImg.size[1])] for j in range(0, self.letterImg.size[0])]
        self.setFrame()
        #print(len(self.letterFrame))
        #print(len(self.letterFrame[0]))
    
    def getFrame(self):
        return self.letterFrame
    def getImage(self):
        return self.letterImg
    
    def getLetter(self):
        return self.letter
    
    def drawWireFrame(self):
        ed = EdgeDetection.EdgeDetection()
        return ed.drawEdges(self.wireFrame, (0,0,255))
    
    ##To compare slopes: start from the middle of the frame and move outward, noting points as you go. Move down some (non-1) increment and do the same, judge the slopes from compare image to letterframe image 
    
    ###MAY WANT TO SWITCH TO USING AVERAGE DISTANCE FROM WIREFRAME INSTEAD OF COUNTING MERGES###
    ##Change accuracy so that it counts how many of image letter's points AREN'T counted too, so that, for example, I (uppercase) isn't considered a T because the T lines up with most of the I whereas I fits perfectly.##
    def compareImagesUsingOverlay(self, compareImg):#returns how accurately the compared letter matches this letter. Problem: on rows with multiple edges, are all returned as true. Still functions, just gives a higher score than it should (algorithm will choose based off of highest score anyway)
        
        img = compareImg.copy()
        #print(img.size[0])
        scaleFactor = float(self.letterImg.size[1])/float(img.size[1])
        img = img.resize((int(compareImg.size[0]*scaleFactor), int(compareImg.size[1]*scaleFactor)))#(self.letterImg.size[0], self.letterImg.size[1]))
        #print(img.size[0])
        #compareImg = compareLetterFrame.getImage()
        compareImage = img.load()
        if float(img.size[0])/float(self.letterImg.size[0]) > 1.4:
            return 1
        elif float(img.size[0])/float(self.letterImg.size[0]) < 0.85:
            return 1
        numWrong = 0
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                if x < len(self.letterFrame) and x < img.size[0] and y < len(self.letterFrame[0]) and y < img.size[1]:
                    
                    if ((self.letterFrame[x][y] == True and compareImage[x,y] == (0,0,0))): #and compareImage[x-1,y] == (0,0,0)) and x+1 < compareImg.size[0] and (self.letterFrame[x][y] == True and compareImage[x+1,y] == (0,0,0)) and (self.letterFrame[x][y] == True and compareImage[x,y] == (0,0,0)):
                        numWrong += 1
                    
                    #elif (self.letterFrame[x][y] == True and compareImage[x,y] == (0,0,0)) :
                      #  numWrong += 1
                        #compareImage[x,y] = (255,0,0)
                    
                    #elif(compareImage[x,y] != (0,0,0) and (not self.pointInFrameIsBounded(x, y))):
                        #numWrong += 1
                        #compareImage[x,y] = (255,0,0)
        #print(numWrong)
        #print("NUM WRONG: " + str(numWrong))
        return float(float(numWrong)/float(self.getNumFramePixels()))#float(1.0-(float(numWrong)/float(self.getNumEdgePixels(compareLetterFrame.getFrame()))))*100.0
    
    def compareImagesUsingOverlayOutput(self, compareImg):#returns how accurately the compared letter matches this letter. Problem: on rows with multiple edges, are all returned as true. Still functions, just gives a higher score than it should (algorithm will choose based off of highest score anyway)
        
        
        #compareImg = compareLetterFrame.getImage()
        #img = compareImg.copy()
        img = compareImg.copy()
        #print(img.size[0])
        scaleFactor = float(self.letterImg.size[1])/float(img.size[1])
        img = img.resize((int(compareImg.size[0]*scaleFactor), int(compareImg.size[1]*scaleFactor)))#(self.letterImg.size[0], self.letterImg.size[1]))
        compareImage = img.load()
        numWrong = 0
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                if x < len(self.letterFrame) and x < img.size[0] and y < len(self.letterFrame[0]) and y < img.size[1]:
                    
                    if (self.letterFrame[x][y] == True and compareImage[x-1,y] == (0,0,0)) and x+1 < img.size[0] and (self.letterFrame[x][y] == True and compareImage[x+1,y] == (0,0,0)) and (self.letterFrame[x][y] == True and compareImage[x,y] == (0,0,0)):
                        numWrong += 1
                        compareImage[x,y] = (255,0,0)
                    #elif (self.letterFrame[x][y] == True and compareImage[x,y] == (0,0,0)) :
                      #  numWrong += 1
                        #compareImage[x,y] = (255,0,0)
                    
                    #elif(compareImage[x,y] != (0,0,0) and (not self.pointInFrameIsBounded(x, y))):
                        #numWrong += 1
                        #compareImage[x,y] = (255,0,0)
        #print(numWrong)
        return img#float(1.0-(float(numWrong)/float(self.getNumEdgePixels(compareLetterFrame.getFrame()))))*100.0
    
    def getNumFramePixels(self):
        num = 0
        for x in range(0, len(self.letterFrame)):
            for y in range(0, len(self.letterFrame[0])):
                #print(self.letterFrame[x][y])
                if self.letterFrame[x][y] == True:
                    num += 1
        return num
    
    def pointInFrameIsBounded(self, pointX, pointY):
        boundPoints = []
        for x in range(0, len(self.letterFrame)):
            if self.letterFrame[x][pointY] == True:
                boundPoints.append(Point.Point(x, pointY))
        
        for i in range(0, len(boundPoints) - 1):
            if pointX > boundPoints[i].getX() and pointX < boundPoints[i+1].getX():
                return True
        return False
                
            
    
    def drawFrame(self):
        ed = EdgeDetection.EdgeDetection()
        return ed.drawEdges(self.letterFrame, (0,0,255))
    
    def drawFrameOntoImage(self, img):
        ed = EdgeDetection.EdgeDetection()
        return ed.drawEdgesOntoImage(img, self.letterFrame, (0,0,255))
    
    def showImage(self):
        self.letterImg.show()
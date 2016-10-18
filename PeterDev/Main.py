'''
Created on Oct 14, 2016

@author: phusisian
'''
from PIL import Image
import time
import os.path
import math
import numpy
from matplotlib.pyplot import colors
from SystemEvents.Standard_Suite import color



img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/targets 300 downScaled2.jpeg")
#img.show()
image = img.load()
dim = img.size



class EdgeDetection:
    
    global colors#defines the list of colors to pull from when color-coding an image
    colors = [(55,114,255), (223,41,53), (253,202,64), (230,232,230)]
    
    def getDColor(self,imgIn):
        imageIn = imgIn.load()
        dColor = [[0 for i in range(imgIn.size[1])] for j in range(imgIn.size[0])]
        height = imgIn.size[1]
        width = imgIn.size[0]
        for y in range(1,height):
            for x in range(1,width):
                currentColor = imageIn[x,y]
                leftColor = imageIn[x-1,y]
                topColor = imageIn[x,y-1]
                dr1 = (currentColor[0]-leftColor[0])**2
                dg1 = (currentColor[1]-leftColor[1])**2
                db1 = (currentColor[2]-leftColor[2])**2
                
                dr2 = (currentColor[0]-topColor[0])**2
                dg2 = (currentColor[1]-topColor[1])**2
                db2 = (currentColor[2]-topColor[2])**2
                
                dColor[x][y] = (math.sqrt(dr1+dg1+db1) + math.sqrt(dr2+dg2+db2))/2.0
        return dColor      
    
    def getSobelEdgeImage(self, dColor, renderType, threshold):
        img = Image.new('RGB', ((len(dColor)), len(dColor[0])))
        image = img.load()
        
        if renderType == "THRESHOLD":
            
            for x in range(0, len(dColor)):
                for y in range(0, len(dColor[0])):
                    if dColor[x][y] > threshold:
                        image[x,y]=(255,255,255)
        elif renderType == "SOFT_EDGES":
            edgeDetection = EdgeDetection()
            highestDColor = edgeDetection.getHighest2DNum(dColor)
            for x in range(0, len(dColor)):
                for y in range(0, len(dColor[0])):
                    colorNum = 255*(dColor[x][y]/highestDColor)
                    image[x,y] = (int(colorNum), int(colorNum), int(colorNum))
        elif renderType == "SOFT_EDGES_THRESHOLD":
            for x in range(0, len(dColor)):
                for y in range(0, len(dColor[0])):
                    if dColor[x][y] > threshold:
                        image[x,y] = (255,255,255)
                    else:
                        colorNum = 255*(dColor[x][y]/threshold)
                        image[x,y] = (int(colorNum), int(colorNum), int(colorNum))
        return img
    
    def getColorCodedImage(self, dColor, renderType, upperThreshold):
        img = Image.new('RGB', ((len(dColor)), len(dColor[0])))
        image = img.load()
        if renderType == "COLOR_CODE_NORMAL":
            edgeDetection = EdgeDetection()
            #highestNum = edgeDetection.getHighest2DNum(dColor)
            for x in range(0, len(dColor)):
                for y in range(0, len(dColor[0])):
                    if dColor[x][y] < upperThreshold:
                        color = colors[(int((len(colors))*(dColor[x][y]/upperThreshold)) )]
                        image[x,y] = color
                    else:
                        image[x,y] = colors[len(colors)-1]
        return img
    
    #might work?
    
    def getD2Color(self,dColor):
        
        d2Color = [[0 for i in range(len(dColor[0]))] for j in range(len(dColor))]
        for y in range(1,len(d2Color[0])):
            for x in range(1,len(d2Color)):
                
                #dr1 = (imageIn[x,y][0]-imageIn[x-1,y][0])**2
                #dg1 = (imageIn[x,y][1]-imageIn[x-1,y][1])**2
                #db1 = (imageIn[x,y][2]-imageIn[x-1,y][2])**2
                
                #dr2 = (imageIn[x,y][0]-imageIn[x,y-1][0])**2
                #dg2 = (imageIn[x,y][1]-imageIn[x,y-1][1])**2
                #db2 = (imageIn[x,y][2]-imageIn[x,y-1][2])**2
                
                d2Color[x][y] = (math.sqrt((dColor[x][y]-dColor[x-1][y])**2) + math.sqrt((dColor[x][y]-dColor[x][y-1])**2))/2.0
                
        return d2Color      
    
    def getD2ColorX(self, dColor):
        d2Color = [[0 for i in range(len(dColor[0]))] for j in range(len(dColor))]
        for y in range(1,len(d2Color[0]) - 1):
            for x in range(1,len(d2Color) - 1):
                #if (dColor[x-1][y] < dColor[x][y] and dColor[x+1][y] < dColor[x][y]) or (dColor[x-1][y] > dColor[x][y] and dColor[x+1][y] > dColor[x][y]):
                if (dColor[x-1][y] < dColor[x][y] and dColor[x+1][y] < dColor[x][y]):
                    d2Color[x][y] = True
                
        return d2Color      
    
    def getD2ColorY(self, dColor):
        d2Color = [[0 for i in range(len(dColor[0]))] for j in range(len(dColor))]
        for y in range(1,len(d2Color[0]) - 1):
            for x in range(1,len(d2Color) - 1):
                #if (dColor[x][y-1] < dColor[x][y] and dColor[x][y+1] < dColor[x][y]) or (dColor[x][y-1] > dColor[x][y] and dColor[x][y+1] > dColor[x][y]):
                if (dColor[x][y-1] < dColor[x][y] and dColor[x][y+1] < dColor[x][y]):
                    d2Color[x][y] = True
                
        return d2Color      

    #not needed?
    def getD2ColorEdgeImageX(self, d2Color):
        img = Image.new('RGB', ((len(dColor)), len(dColor[0])))
        image = img.load()
        for y in range(1,len(d2Color[0])):
            for x in range(1,len(d2Color)):
                if d2Color[x][y] == True:
                    image[x,y] = (255,255,255)
        return img
    
    def getD2EdgeImage(self, d2ColorX, d2ColorY):
        img = Image.new('RGB', ((len(dColor)), len(dColor[0])))
        image = img.load()
        for y in range(1,len(d2ColorX[0])):
            for x in range(1,len(d2ColorX)):
                if d2ColorX[x][y] == True:
                    image[x,y] = (255,255,255)
                elif d2ColorY[x][y] == True:
                    image[x,y] = (255,255,255)
        return img
                
    def getHighest2DNum(self, list):
        highestNum = list[0][0]
        for i in range(0, len(list)):
            for j in range(0, len(list[0])):
                if list[i][j] > highestNum:
                    highestNum = list[i][j]
        return highestNum
    
    def drawRect(self, imgIn, xIn, yIn, width, height, color):
        
        image = imgIn.load()
        for x in range(xIn, xIn+width):
            image[x,yIn] = color
            image[x,yIn+height] = color
        for y in range(yIn, yIn+height):
            image[xIn, y] = color
            image[xIn+width, y] = color
     
    def shadeSobelShape(self, imgIn, dColor, threshold, xIn, yIn, width, height, color):
        edgeDetection = EdgeDetection()
        edgeDetection.drawRect(imgIn,xIn, yIn, width, height, (0,0,255))
        
        pointArray = [[0 for j in range(0,2)] for i in range(imgIn.size[1])]
        pointArrayCount = 0
        image = imgIn.load()
        for y in range(yIn, yIn+height):   
            points = [0 for i in range(0,2)]
            edgeFound = False
            insideFound = False
            pointCount = 0
            for x in range(xIn, xIn+width):
                if pointCount < 2:
                    if edgeFound == False:
                        if dColor[x][y] > threshold:
                            points[pointCount] = Point(x,y)
                            edgeFound = True
                            pointCount += 1
                    else:
                        if insideFound == False:
                            if dColor[x][y] < threshold:
                                insideFound = True
                                edgeFound = False
            if pointCount >= 2:
                pointArray[pointArrayCount] = points
                pointArrayCount += 1
                for x in range(points[0].getX(), points[1].getX()):
                    image[x,y] = color
        
        boundsX = edgeDetection.getPointXBounds(pointArray)
        boundsY = edgeDetection.getPointYBounds(pointArray)
        
        edgeDetection.drawRect(imgIn, boundsX[0], boundsY[0], boundsX[1]-boundsX[0], boundsY[1]-boundsY[0], color)
        
        return imgIn
    
    def getPointXBounds(self, points):
        smallestX = points[0][0].getX()
        biggestX = points[0][1].getX()
        for i in range(0, len(points)):
            if points[i][0]!=0:
                if points[i][0].getX() < smallestX:
                    smallestX = points[i][0].getX()
                if points[i][1].getY() > biggestX:
                    biggestX = points[i][1]
        return[smallestX, biggestX]
    
    def getPointYBounds(self, points):
        topY = points[0][0].getY()
        bottomY = points[0][0].getY()
        for i in range(0, len(points)):
            if points[i][0] != 0:
                topY = points[i][0].getY()
                break
        for i in range(len(points)-1, 0, -1):
            if points[i][0] != 0:
                bottomY = points[i][0].getY()
                break
        return [topY, bottomY]
    
    def removeLowerDColorThreshold(self, dColor, threshold):
        edgeDetection = EdgeDetection()
        highestDColor = edgeDetection.getHighest2DNum(dColor)
        for x in range(0, len(dColor)):
            for y in range(0, len(dColor[0])):
                if dColor[x][y] < threshold:
                    dColor[x][y] = 0
        return dColor   
    
class Point:
    def __init__(self, xIn, yIn): 
        self.x = xIn
        self.y = yIn
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self, xIn):
        self.x=xIn
    def setY(self, yIn):
        self.y=yIn
           

class ImageEdit:
    def drawRect(self, imgIn, xIn, yIn, width, height, color):
        
        image = imgIn.load()
        for x in range(xIn, xIn+width):
            image[x,yIn] = color
            image[x,yIn+height] = color
        for y in range(yIn, yIn+height):
            image[xIn, y] = color
            image[xIn+width, y] = color
     
    def fillRect(self, imgIn, xIn, yIn, width, height, color):
        image = imgIn.load()
        for x in range(xIn, xIn+width):
            for y in range(yIn, yIn+height):
                image[x,y] = color
    

class ObjectDetection:
    
    #doesn't work as well as boundObjectsAVG
    def boundObjects(self, imgIn, dColor, percentThreshold, threshold, chunksWidth, chunksHeight):
        image = imgIn.load()
        dColor = numpy.array(dColor)
        #print(dColor)
        ie = ImageEdit()
        chunkWidth = imgIn.size[0]/chunksWidth
        chunkHeight = imgIn.size[1]/chunksHeight
        od = ObjectDetection()
        for x in range(0, chunksWidth):
            for y in range(0, chunksHeight):
                #ie.fillRect(imgIn, x*chunkWidth, y*chunkHeight, chunkWidth, chunkHeight, (255,0,0))
                
                if od.getPercentUnderThreshold2D(dColor[(x*chunkWidth):(x*chunkWidth + chunkWidth),(y*chunkHeight):(y*chunkHeight + chunkHeight)], threshold) > percentThreshold:
                    ie.fillRect(imgIn, x*chunkWidth, y*chunkHeight, chunkWidth, chunkHeight, (0,0,255))
                #else:
                   # numOff = od.getPercentUnderThreshold2D(dColor[(x*chunkWidth):(x*chunkWidth + chunkWidth),(y*chunkHeight):(y*chunkHeight + chunkHeight)], threshold)
                    #print(numOff)
                    #color = (int(255*numOff),0,255-int(255*numOff))
                    #ie.fillRect(imgIn, x*chunkWidth, y*chunkHeight, chunkWidth, chunkHeight, color)
        return imgIn
    
    def boundObjectsAVG(self, imgIn, dColor, threshold, chunksWidth, chunksHeight):
        image = imgIn.load()
        dColor = numpy.array(dColor)
        #print(dColor)
        ie = ImageEdit()
        chunkWidth = imgIn.size[0]/chunksWidth
        chunkHeight = imgIn.size[1]/chunksHeight
        od = ObjectDetection()
        for x in range(0, chunksWidth):
            for y in range(0, chunksHeight):
                #ie.fillRect(imgIn, x*chunkWidth, y*chunkHeight, chunkWidth, chunkHeight, (255,0,0))
                #if od.getAverage2DValue(dColor[(x*chunkWidth):(x*chunkWidth + chunkWidth),(y*chunkHeight):(y*chunkHeight + chunkHeight)]) < threshold:
                if od.getAverage2DValue(dColor[(x*chunkWidth):(x*chunkWidth + chunkWidth),(y*chunkHeight):(y*chunkHeight + chunkHeight)]) <threshold:
                    ie.fillRect(imgIn, x*chunkWidth, y*chunkHeight, chunkWidth, chunkHeight, (0,0,255))
        return imgIn
    
    def paintAllDColorUnder(self, imgIn, dColor, threshold, upperThreshold):
        image = imgIn.load()
        for x in range(0, imgIn.size[0]):
            for y in range(0, imgIn.size[1]):
                if dColor[x][y] < threshold:
                    image[x,y] = (255,0,0)
                elif dColor[x][y] < upperThreshold:
                    image[x,y] = (255,0,int(255*float((dColor[x][y]-threshold)/(upperThreshold-threshold))))
        return imgIn
    
    def getObjArrayUsingDColorUnder(self, dColor, threshold, upperThreshold):
        
        objArr = [[0 for j in range(0,len(dColor[0]))] for i in range(0,len(dColor))]
        for x in range(0, len(objArr)):
            for y in range(0, len(objArr[1])):
                if dColor[x][y] < threshold:
                    objArr[x][y] = 1
                elif dColor[x][y] < upperThreshold:
                    objArr[x][y] = 0.85
        return objArr
    
    def fillObjArr(self, imgIn, objArr, chunksWidth, chunksHeight, avg):
        image = imgIn.load()
        ie = ImageEdit()
        objDetect = ObjectDetection()
        objArr = numpy.array(objArr)
        chunkWidth = imgIn.size[0]/chunksWidth
        chunkHeight = imgIn.size[1]/chunksHeight
        for x in range(0, chunksWidth-1):
            for y in range(0, chunksHeight-1):
                if objDetect.getAverage2DValue(objArr[(x*chunkWidth):(x*chunkWidth + chunkWidth),(y*chunkHeight):(y*chunkHeight + chunkHeight)]) > avg:#is 0.5 because currently it's either 1 or 0.5
                    ie.fillRect(imgIn, x*chunkWidth, y*chunkHeight, chunkWidth-1, chunkHeight-1, (0,0,255))
        return imgIn
    
    def getPercentGreaterThan2D(self, listIn, threshold):
        add = 0
        area = len(listIn)*len(listIn[0])
        for i in range(0, len(listIn)):
            for j in range(0, len(listIn[0])):
                if listIn[i][j] >= threshold:
                    add +=1
        return float(float(add)/float(area))
    
    def getPercentUnderThreshold2D(self, listIn, threshold):
        add = 0
        area = len(listIn)*len(listIn[0])
        for i in range(0, len(listIn)):
            for j in range(0, len(listIn[0])):
                if listIn[i][j] < threshold:
                    add +=1
        return float(float(add)/float(area))
    #doesn't work???
    def getAverage2DValue(self, listIn):
        
        add = 0
        area = len(listIn)*len(listIn[0])
        if area > 0:
            #print(area)
            for i in range(0, len(listIn)):
                for j in range(0, len(listIn[0])):
                    add += listIn[i][j]
            return float(float(add)/float(area))
        return 0
start = time.time()
edgeDetection = EdgeDetection()
dColor = edgeDetection.getDColor(img)
objDetect = ObjectDetection()
edgeDetection.removeLowerDColorThreshold(dColor, 20)
d2ColorX = edgeDetection.getD2ColorX(dColor)
d2ColorY = edgeDetection.getD2ColorY(dColor)
b=edgeDetection.getD2EdgeImage(d2ColorX, d2ColorY)
objArr = objDetect.getObjArrayUsingDColorUnder(dColor, 3, 8)
#b=objDetect.fillObjArr(b, objArr, 480, 320, 0.85)
#b=edgeDetection.getSobelEdgeImage(dColor, "SOFT_EDGES_THRESHOLD", 70)
#b=edgeDetection.getColorCodedImage(dColor, "COLOR_CODE_NORMAL", 15)
#b=objDetect.boundObjectsAVG(img, dColor, 2, 25,25)

#b = objDetect.paintAllDColorUnder(b, dColor, 3, 6.5)
#b=objDetect.boundObjects(img, dColor, 0.6, 5, 240,160)
b.show()

print(time.time()-start)

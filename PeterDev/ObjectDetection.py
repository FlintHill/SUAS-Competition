import EdgeDetection
from PIL import Image
import Rectangle
import Paint
import ArrayHelper

class ObjectDetection:
    
    global shadeColors
    shadeColors = [(255,0,0), (255,255,0), (0,255,255), (0,255,0), (0,0,255), (255,255,255)]#list of colors used to shade layer by layer. If exceeded, reverts to the lowest index and reuses the color.
    
    def drawBoundedObjects(self, imgIn, edges, clipRect):###In place for sake of human understandability. Possibly dumb to use when you can fill the layers array using fillLayers####could save the multiple colors denoting new edges as layers so I could look at individual layers, allowing me to even crop out letters or only the shape
        edgeDetect = EdgeDetection.EdgeDetection()
        paint = Paint.Paint()
        
        for y in range(clipRect.getY(), clipRect.getY() + clipRect.getHeight()):
            
            edgePoints = edgeDetect.getEdgesAtRow(edges, y)
            
            if edgePoints != False and len(edgePoints)%2 == 0:#if there are edges on this row and there are an EVEN number (becomes problematic when just a corner clips into the row because it can't tell that it's just a corner -- doesn't know where one shape's edge ends and the other begins)"
                
                for pointNum in range(0, len(edgePoints) - 1):
                    if pointNum < len(edgePoints)/2.0:
                        color = shadeColors[pointNum%len(shadeColors)]
                        paint.drawHorizontalLine(imgIn, edgePoints[pointNum].getX(), edgePoints[pointNum].getY(), edgePoints[pointNum + 1].getX() - edgePoints[pointNum].getX(), color)
                    else:
                        color = shadeColors[(len(edgePoints)-2-pointNum)%len(shadeColors)]
                        paint.drawHorizontalLine(imgIn, edgePoints[pointNum].getX(), edgePoints[pointNum].getY(), edgePoints[pointNum + 1].getX() - edgePoints[pointNum].getX(), color)
                
        for x in range(clipRect.getX() , clipRect.getX() + clipRect.getWidth()):#Optimization: Scans over twice (left to right, top to bottom) instead of just filling in the empty lines
            
            edgePoints = edgeDetect.getEdgesAtColumn(edges, x)
            
            if edgePoints != False and len(edgePoints)%2 == 0:
                for pointNum in range(0, len(edgePoints)-1):
                    if pointNum < len(edgePoints)/2.0:
                        color = shadeColors[pointNum%len(shadeColors)]
                        paint.drawVerticalLine(imgIn, edgePoints[pointNum].getX(), edgePoints[pointNum].getY(), edgePoints[pointNum+1].getY() - edgePoints[pointNum].getY(), color)
                    else:
                        color = shadeColors[(len(edgePoints)-2-pointNum)%len(shadeColors)]
                        paint.drawVerticalLine(imgIn, edgePoints[pointNum].getX(), edgePoints[pointNum].getY(), edgePoints[pointNum+1].getY() - edgePoints[pointNum].getY(), color)
        return imgIn
    
    def getImageLayers(self, edges, clipRect):#Returns a 2D array of integers representing the image's layers within a rectangle that bounds the output#could be faster instead of re-going-over already filled rows
        edgeDetect = EdgeDetection.EdgeDetection()
        arrHelp = ArrayHelper.ArrayHelper()
        layers = [[0 for y in range(0, len(edges[1]))] for x in range(0, len(edges[0]))]
        
        for y in range(clipRect.getY(), clipRect.getY() + clipRect.getHeight()):
            edgePoints = edgeDetect.getEdgesAtRow(edges, y)
            
            if edgePoints != False and len(edgePoints)%2 == 0:
                
                for pointNum in range(0, len(edgePoints) - 1):
                    
                    if pointNum < len(edgePoints)/2.0:
                        value = pointNum + 1
                        arrHelp.fillHorizontalLine(layers, value, edgePoints[pointNum].getX(), edgePoints[pointNum].getY(), edgePoints[pointNum + 1].getX() - edgePoints[pointNum].getX())
                    else:
                        value = (len(edgePoints)-2-pointNum) + 1
                        arrHelp.fillHorizontalLine(layers, value, edgePoints[pointNum].getX(), edgePoints[pointNum].getY(), edgePoints[pointNum + 1].getX() - edgePoints[pointNum].getX())
              
        for x in range(clipRect.getX() , clipRect.getX() + clipRect.getWidth()):#Optimization: Scans over twice (left to right, top to bottom) instead of just filling in the empty lines
            
            edgePoints = edgeDetect.getEdgesAtColumn(edges, x)
            
            if edgePoints != False and len(edgePoints)%2 == 0:
                
                for pointNum in range(0, len(edgePoints)-1):
                    if pointNum < len(edgePoints)/2.0:
                        value = pointNum + 1
                        arrHelp.fillVerticalLineIfEmpty(layers, value, 0, edgePoints[pointNum].getX(), edgePoints[pointNum].getY(), edgePoints[pointNum+1].getY() - edgePoints[pointNum].getY())
                    else:
                        value = (len(edgePoints)-2-pointNum) + 1
                        arrHelp.fillVerticalLineIfEmpty(layers, value, 0, edgePoints[pointNum].getX(), edgePoints[pointNum].getY(), edgePoints[pointNum+1].getY() - edgePoints[pointNum].getY())
                        
        return layers
    
    def fillLayers(self, layers):#outputs a filled-in image color-coded by layer using the shadedColors list.
        img = Image.new("RGB", (len(layers), len(layers[0])))
        image = img.load()
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                image[x,y] = shadeColors[layers[x][y] % len(shadeColors)]
                
        return img
    
    def fillLayer(self, layers, layerNum, color):#outputs an image with only one layer filled which is specified by "layerNum"
        img = Image.new("RGB", (len(layers), len(layers[0])))
        image = img.load()
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                if layers[x][y] == layerNum:
                    image[x,y] = color
        return img
        
    def getLayerBounds(self, layers, layerNum):#returns a Rectangle object that bounds the outside of the layer specified by "layerNum"
        leftX = len(layers)
        rightX = 0
        topY = len(layers[0])
        bottomY = 0
        for x in range(0, len(layers)):
            for y in range(0, len(layers[0])):
                if layers[x][y] == layerNum:
                    if x < leftX:
                        leftX = x
                    if y < topY:
                        topY = y
                    if y > bottomY:
                        bottomY = y
                    if x > rightX:
                        rightX = x
        return Rectangle.Rectangle(leftX, topY, rightX-leftX, bottomY-topY)
        
        
        
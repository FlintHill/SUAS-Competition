'''
Created on Nov 6, 2016

@author: phusisian
'''

from PIL import Image
import EdgeDetection
import Rectangle
import ObjectDetection
import Paint
class CharacterCropper:
    global defaultLayer
    defaultLayer = 2
    
    def __init__(self, imgIn):
        self.img = imgIn
        self.image = self.img.load()
    
    def getSeparatedColorImages(self):
        colors = self.getColorsInImage()
        imgs = [Image.new("RGB", [self.img.size[0], self.img.size[1]]) for j in range(0, len(colors))]
        images= []
        
        for i in range(0, len(imgs)):
            images.append(imgs[i].load())
        
        for i in range(0, len(colors)):
            for x in range(0, self.img.size[0]):
                for y in range(0, self.img.size[1]):
                    if self.image[x,y] == colors[i]:
                        images[i][x,y] = self.image[x,y]
        
        return imgs
    
    def getColorsInImage(self):
        colors = []
        for x in range(0, self.img.size[0]):
            for y in range(0, self.img.size[1]):
                if len(colors) != 0:
                    newColor = True
                    for i in range(0, len(colors)):
                        if self.image[x,y] == colors[i]:
                            newColor= False
                    
                    if newColor == True:
                        colors.append(self.image[x,y])
                else:
                    colors.append(self.image[x,y])
        return colors
    
    def getLetterCropImage(self): #NOTE: Rotation is by an arbitrary amount for testing purposes. The drone will be able to keep track of its rotation so it will know the correct amount to rotate the image, but for now I have put it in manually
        colors = self.getColorsInImage()
        sepImages = self.getSeparatedColorImages()
        backgroundColor = self.getBackgroundColor()
        shapeImg = 0
        #shapeImage = 0
        shapeColor = self.getShapeColor()
        #for i in range(0, len(colors)):
         #   if colors[i] == shapeColor:
          #      return sepImages[i]
        shapeImg = self.fillOuterEdges(self.inverseLayer(sepImages[len(sepImages)-1], (0,0,0), (255,255,255)) ).rotate(50)    
        bounds = self.getCharacterBounds(shapeImg, (255,255,255))
        shapeImg = shapeImg.crop((bounds.getX(), bounds.getY(), bounds.getX() + bounds.getWidth(), bounds.getY() + bounds.getHeight()))
        return shapeImg
        #shapeImage = shapeImg.load()
        #self.inverseLayer(shapeImg)
        #return shapeImg
        
                #return sepImages[i]
        #return None
    
    def subtractLayer(self, baseLayerIn, subtractLayerImgIn, subtractColor):
        baseImage = baseLayerIn.load()
        subtractImage = subtractLayerImgIn.load()
        
        for x in range(0, subtractLayerImgIn.size[0]):
            for y in range(0, subtractLayerImgIn.size[1]):
                if subtractImage[x,y] != subtractColor:
                    baseImage[x,y] = subtractColor
                    
        return baseLayerIn
    
    def inverseLayer(self, layerImgIn, baseColor, topColor):
        image = layerImgIn.load()
        for x in range(0, layerImgIn.size[0]):
            for y in range(0, layerImgIn.size[1]):
                if image[x,y] == (0,0,0):
                    image[x,y] = topColor
                else: 
                    image[x,y] = baseColor
                #image[x,y] = (255-image[x,y][0], 255-image[x,y][1], 255-image[x,y][2])  
        return layerImgIn
    
    '''
    def removeCharacterImageNoise(self, imgIn):
        image = imgIn.load()
        edges = EdgeDetection.EdgeDetection().getKMeansEdges(imgIn)
        layers = ObjectDetection.ObjectDetection().getImageLayers(edges, Rectangle.Rectangle(0,0, imgIn.size[0], imgIn.size[1]))
        return ObjectDetection.ObjectDetection().fillLayer(layers, 3, (255,255,255))
    '''
    
    def fillOuterEdges(self, imgIn):
        image = imgIn.load()
        ed = EdgeDetection.EdgeDetection()
        edges = ed.getKMeansEdges(imgIn)
        paint = Paint.Paint()
        ed.drawEdges(edges, (255,0,0)).show()
        for i in range(0, len(edges[0])):
            rowEdges = ed.getEdgesAtRow(edges,i)
            if len(rowEdges)> 1:
                paint.drawHorizontalLine(imgIn,0, i, rowEdges[0].getX(), (0,0,0))
                paint.drawHorizontalLine(imgIn, rowEdges[len(rowEdges)-1].getX() - 5, i, imgIn.size[0]-rowEdges[len(rowEdges)-1].getX() + 5, (0,0,0) ) #-5 here just so that it fully covers the edge. arbitrary number. possible that an edge could be off by more than that so that the image output is still incorrect
            else:
                paint.drawHorizontalLine(imgIn, 0, i, imgIn.size[0], (0,0,0))
        return imgIn
        
        
    def getCharacterBounds(self, imgIn, color):#returns a Rectangle object that bounds the outside of the layer specified by "layerNum"
        image = imgIn.load()
        leftX = imgIn.size[0]
        rightX = 0
        topY = imgIn.size[1]
        bottomY = 0
        for x in range(0, imgIn.size[0]):
            for y in range(0, imgIn.size[1]):
                if image[x,y] == color:
                    if x < leftX:
                        leftX = x
                    if y < topY:
                        topY = y
                    if y > bottomY:
                        bottomY = y
                    if x > rightX:
                        rightX = x
        return Rectangle.Rectangle(leftX, topY, rightX-leftX, bottomY-topY)
    
    def getBackgroundColor(self):
        return self.image[0,0]

    def getShapeColor(self):
        backgroundColor = self.getBackgroundColor
        for x in range(0, self.img.size[0]):
            for y in range(0, self.img.size[1]):
                if self.image[x,y] != backgroundColor:
                    return backgroundColor
        return None
        
'''
Created on Nov 3, 2016

@author: phusisian
'''
from SystemEvents.Standard_Suite import color
class Paint:
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

    def drawHorizontalLine(self, imgIn, x, y, width, color):
        image = imgIn.load()
        for i in range(x, x+width):
            image[i,y] = color
        return imgIn
    
    def drawVerticalLine(self, imgIn, x, y, height, color):
        image = imgIn.load()
        for i in range(y, y+height):
            image[x, i] = color
        return imgIn
    
    def drawRectangle(self, imgIn, rect, color):
        paint = Paint()
        paint.drawHorizontalLine(imgIn, rect.getX(), rect.getY(), rect.getWidth(), color)
        paint.drawHorizontalLine(imgIn, rect.getX(), rect.getY()+rect.getHeight(), rect.getWidth(), color)
        paint.drawVerticalLine(imgIn, rect.getX(), rect.getY(), rect.getHeight(), color)
        paint.drawVerticalLine(imgIn, rect.getX() + rect.getWidth(), rect.getY(), rect.getHeight(), color)
        return imgIn
        
    def superimposeImage(self, bottomImg, topImg):
        bottomImage = bottomImg.load()
        topImage = topIma.load()
        for x in range(0, topImg.size[0]):
            for y in range(0, topImg.size[1]):
                bottomImage[x,y]=topImage[x,y]
        return bottomImage
        
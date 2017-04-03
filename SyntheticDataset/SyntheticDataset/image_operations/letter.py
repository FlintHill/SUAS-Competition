import numpy
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import math
from math import degrees
from SyntheticDataset.color import *
from SyntheticDataset.image_operations import *
import random

class Letter(object):
    '''this is the ratio of one pixel of font height to what font size is required. Has to be changed if font is changed.
    in the future I would set this on a per-font basis using a class, because the math isn't very difficult
    (type a letter out into a big frame, divide the font size by its actual height)'''
    fontRatio = 1.44230769230769

    def __init__(self, boundFieldObjectIn, letterIn, fontIn, pixelHeightIn):
        self.boundFieldObject = boundFieldObjectIn
        self.letterColor = ColorList.getRandomColorExcludingClosestToBackground(self.boundFieldObject.getColor())#ColorList.getRandomColor()[1]
        self.fontSize = int(pixelHeightIn*Letter.fontRatio)#this will convert the pixel height into the correct font. The ratio will have to be recalculated and changed if the font is changed
        self.font = ImageFont.truetype(fontIn, self.fontSize)#need to find the ratio of font size to pixel height on a per-font basis so the typed letter will always fit in the shape
        self.pixelHeight = pixelHeightIn

        self.letter = letterIn
        self.setLetterImg()
        letterBounds = ImageBounder.getBoundsOfColor(self.letterImg, self.letterImage, self.letterColor)
        self.letterBounds = letterBounds
        self.letterImg = ImageCropper.cropImgToRect(self.letterImg, letterBounds)
        self.setGradientLetterImg()

    def setGradientLetterImg(self):
        self.grayGradientMaker = GrayGradientMaker(self.letterImg.size, .05)
        self.gradientLetterImg = self.letterImg.copy()
        self.grayGradientMaker.applyGradients(self.gradientLetterImg, self.gradientLetterImg.load())

        self.gradientLetterImg = GaussianBlur.getGaussianFilteredImg(self.gradientLetterImg, self.gradientLetterImg.load(), 3, 1)

    def getLetterImg(self):
        return self.letterImg

    def getDim(self):
        return self.letterImg.size

    def showLetterImg(self):
        self.letterImg.show()

    def getLetter(self):
        return self.letter

    def getMidpoint(self):
        return Point(self.letterImg.size[0]/2, self.letterImg.size[1]/2)

    def getColor(self):
        return self.letterColor

    def getGradientLetterImg(self):
        return self.gradientLetterImg

    def setLetterImg(self):
        backgroundColor = (self.boundFieldObject.getColor()[0], self.boundFieldObject.getColor()[1], self.boundFieldObject.getColor()[2], 0)

        self.letterImg = Image.new("RGBA", (self.pixelHeight, self.pixelHeight*3), backgroundColor)#multiplying the width by three just gives some leeway for bigger letters like M and W
        draw = ImageDraw.Draw(self.letterImg)
        draw.fontmode = "0" #one sets to not antialias. If camera antialiases, set to zero.
        draw.text((1,1), self.letter, self.letterColor, font = self.font)
        self.unrotatedLetterImg = self.letterImg.copy()
        self.letterImg = self.letterImg.rotate(degrees(self.boundFieldObject.getRotation()), expand=True)
        tempImg = Image.new('RGBA', self.letterImg.size, (backgroundColor))#this is here because when the image is rotated, the background color (with alpha zero for guassian blur) is removed. This image is pasted to with the other, which lost the color it used to have as a background
        tempImg.paste(self.letterImg, (0,0), self.letterImg)
        self.letterImg = tempImg
        self.letterImage = self.letterImg.load()

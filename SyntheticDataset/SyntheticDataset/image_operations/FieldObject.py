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

class FieldObject(object):
    grassColor = (1,142,14,0)
    lowerLetterRadiusBound = 0.55
    upperLetterRadiusBound = 1

    #possibleShapes = ["triangle", "square", "rectangle", "pentagon", "hexagon", "heptagon", "octagon", "circle", "semicircle", "quartercircle"]
    '''excluding some of the shapes it messes up on for now'''
    possibleShapes = ["Triangle", "Square", "Rectangle", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Circle"]

    '''semicircles and quartercircles not working properly. (are rotated off the field)'''
    def __init__(self, shapeTypeIn, boundingBoxIn, rotationIn, colorIn, letterIn):
        self.shapeType = shapeTypeIn
        self.bounds = boundingBoxIn
        self.midpoint = self.getMidpointFromBounds()
        self.radius = self.getRadiusFromBounds()
        self.rotation = rotationIn
        self.color = colorIn
        self.setPolygon()
        self.grayGradient = GrayGradientMaker((self.polygon.getBoundsWithMargin(Polygon.defaultMaskMargin).getWidth(), self.polygon.getBoundsWithMargin(Polygon.defaultMaskMargin).getHeight()), .04)
        self.setObjectLetter(letterIn)

    def setObjectLetter(self, letter):
        randomHeight = int((FieldObject.lowerLetterRadiusBound + random.random()*(FieldObject.upperLetterRadiusBound - FieldObject.lowerLetterRadiusBound))*self.radius)
        self.objectLetter = ObjectLetter(self, letter,"/Users/vtolpegin/github/SUAS-Competition/SyntheticDataset/fonts/Blockletter.otf", randomHeight)#eventually replace the letter size with a method that gets a random height within reasonable bounds

    def __repr__(self):
        repString = "orientation: " + CompassAngler.getClosestCompassAngle(self.rotation) + "\n"
        repString += "shape: " + self.shapeType + "\n"
        repString += "background_color: " + ColorList.getClosestColorsName(self.color) + "\n"
        repString += "alphanumeric: " + self.objectLetter.getLetter() + "\n"
        repString += "alphanumeric_color: " + ColorList.getClosestColorsName(self.objectLetter.getColor())

        return repString

    def asNumpy(self):
        return numpy.asarray((CompassAngler.getClosestCompassAngle(self.rotation), self.shapeType, ColorList.getClosestColorsName(self.color), self.objectLetter.getLetter(), ColorList.getClosestColorsName(self.objectLetter.getColor())))

    def setPolygon(self): #no trapezoid, cross, or star support yet.Rotations are clockwise for some reason in SimplePolygonMaker, so that's why self.rotation is negative on polygon creation.
        radius = self.getRadiusFromBounds()
        if self.shapeType in FieldObject.possibleShapes:
            if self.shapeType == "Triangle":
                self.polygon = SimplePolygonMaker.createTriangleInt(self.midpoint, self.radius, -self.rotation)
            elif self.shapeType == "Square":
                self.polygon = SimplePolygonMaker.createSquareInt(self.midpoint, self.radius, -self.rotation)
            elif self.shapeType == "Rectangle":
                self.polygon = SimplePolygonMaker.createRectangleInt(self.midpoint, self.bounds.getWidth(), self.bounds.getHeight(), -self.rotation)
            elif self.shapeType == "Pentagon":
                self.polygon = SimplePolygonMaker.createPentagonInt(self.midpoint, self.radius, -self.rotation)
            elif self.shapeType == "Hexagon":
                self.polygon = SimplePolygonMaker.createHexagonInt(self.midpoint, self.radius, -self.rotation)
            elif self.shapeType == "Heptagon":
                self.polygon = SimplePolygonMaker.createHeptagonInt(self.midpoint, self.radius, -self.rotation)
            elif self.shapeType == "Octagon":
                self.polygon = SimplePolygonMaker.createOctagonInt(self.midpoint, self.radius, -self.rotation)
            elif self.shapeType == "Circle":
                self.polygon = SimplePolygonMaker.createCircleInt(self.midpoint, self.radius)
            elif self.shapeType == "Semi-Circle":
                self.polygon = SimplePolygonMaker.createSemicircleInt(self.midpoint, self.radius, -self.rotation)
            elif self.shapeType == "Quarter-Circle":
                self.polygon = SimplePolygonMaker.createQuartercircleInt(self.midpoint, self.radius, -self.rotation)
        else:
                raise ValueError("Shape type not supported")

    def getPolygon(self):
        return self.polygon

    def fill(self, img, image):
        maskImg = self.polygon.getFilledMask(self.polygon.getBoundsWithMargin(Polygon.defaultMaskMargin), (0,0,0))
        margin = 10
        pasteMaskImg = Image.new('RGBA', (maskImg.size[0] + margin * 2, maskImg.size[1] + margin*2), (0,0,0,0))#this is created so that drop shadow has enough space to fuzz the edges
        pasteMaskImg.paste(maskImg, (margin, margin), maskImg)
        pasteMaskImg = GaussianBlur.getGaussianFilteredImgWithAlpha(pasteMaskImg, pasteMaskImg.load(), 5, 7)#this needs to be adjusted based on shape size, bigger shapes need bigger drop shadow.

        pasteShapeImg = self.polygon.getGradientFilledMask(self.polygon.getBoundsWithMargin(Polygon.defaultMaskMargin), self.color, self.grayGradient)#fillWithGradient(img, image, self.color, self.grayGradient)
        tempImg = Image.new('RGBA', pasteShapeImg.size, FieldObject.grassColor)
        tempImg.paste(pasteShapeImg, (0,0), pasteShapeImg)
        pasteShapeImg = tempImg
        pasteShapeImg = GaussianBlur.getGaussianFilteredImg(pasteShapeImg, pasteShapeImg.load(), 3, .8)

        pasteMaskImg.paste(pasteShapeImg, (margin, margin), pasteShapeImg)
        newBounds = self.polygon.getBoundsWithMargin(Polygon.defaultMaskMargin + margin)
        img.paste(pasteMaskImg, (newBounds.getX(), newBounds.getY()), pasteMaskImg)
        self.pasteLetterImg(img)
        return None

    def getRotation(self):
        return self.rotation

    def pasteLetterImg(self, img):
        letterMidpoint = self.objectLetter.getMidpoint()
        polyMidpoint = self.polygon.getMidpoint().toInt()
        translatePoint = letterMidpoint.getTranslatePoint(polyMidpoint).toInt()
        img.paste(self.objectLetter.getGradientLetterImg(), (translatePoint.getX(), translatePoint.getY()), self.objectLetter.getGradientLetterImg())
        return None

    def getMidpointFromBounds(self):
        if self.shapeType != "semicircle" and self.shapeType != "quartercircle":
            return Point(self.bounds.getX() + self.bounds.getWidth()/2, self.bounds.getY() + self.bounds.getHeight()/2)
        elif self.shapeType == "semicricle":
            return Point(self.bounds.getX() + self.bounds.getWidth()/2, self.bounds.getY() + self.bounds.getHeight()/2)
        else:
            return Point(self.bounds.getX(), self.bounds.getY() + self.bounds.getHeight())

    def getRadiusFromBounds(self):
        if self.bounds.getWidth() < self.bounds.getHeight():
            return self.bounds.getWidth()/2
        else:
            return self.bounds.getHeight()/2

    def getColor(self):
        return self.color

class CompassAngler(object):
    COMPASS_ANGLES = [("E", 0), ("NE", math.pi/4.0), ("N", math.pi/2.0), ("NW", 3.0*math.pi/4.0), ("W", math.pi), ("SW", 5.0*math.pi/4.0), ("S", 3.0*math.pi/2.0), ("SE", 7.0*math.pi/4.0), ("E", 2.0*math.pi)]

    @staticmethod
    def getClosestCompassAngle(angle):
        sorted_angles = CompassAngler.getCompassAnglesSortedByProximityToAngle(angle)#sorted(AngleRounder.COMPASS_ANGLES, key = lambda compass_angle : abs(compass_angle[1]-angle)%(2.0*pi))
        return sorted_angles[0][0]
    #compassAngles = [('E', 0), ('NE', math.pi/4.0), ('N', math.pi/2.0), ('NW', 3.0*math.pi/4.0), ('W', math.pi), ('SW', 5.0*math.pi/4.0), ('S', 3.0*math.pi/2.0), ('SE', 7.0*math.pi/4.0), ('N', 2.0*math.pi)]
    '''doesn't correct for input angle to be in 0 to 2pi because I'd assume I'd only generate angles within those bounds'''
    '''@staticmethod
    def getClosestCompassAngle(angle):
        leastDifferenceIndex = 0
        leastDifference = abs(CompassAngler.compassAngles[0][1] - angle)
        for i in range(0, len(CompassAngler.compassAngles)):
            incDifference = abs(CompassAngler.compassAngles[i][1] - angle)%(math.pi*2.0)
            if incDifference < leastDifference:
                leastDifference = incDifference
        return CompassAngler.compassAngles[leastDifferenceIndex][0]
    '''

    @staticmethod
    def getCompassAnglesSortedByProximityToAngle(angle ):
        unrotatedAngle = (angle + (math.pi/2.0))%(2.0*math.pi)
        if unrotatedAngle < 0:
            unrotatedAngle += 2.0*math.pi
        #print("angle in: " + str(angle))
        print("rounded angle: " + str(sorted(CompassAngler.COMPASS_ANGLES, key = lambda compass_angle : abs((unrotatedAngle - compass_angle[1]))%(2.0*math.pi))[0]))
        return sorted(CompassAngler.COMPASS_ANGLES, key = lambda compass_angle : abs((unrotatedAngle - compass_angle[1]))%(2.0*math.pi))

    @staticmethod
    def getRandomCompassAngle():
        randIndex = random.randint(0, len(CompassAngler.compassAngles) - 1)
        return CompassAngler.compassAngles[randIndex][1]

class ObjectLetter(object):
    '''this is the ratio of one pixel of font height to what font size is required. Has to be changed if font is changed.
    in the future I would set this on a per-font basis using a class, because the math isn't very difficult
    (type a letter out into a big frame, divide the font size by its actual height)'''
    fontRatio = 1.44230769230769

    def __init__(self, boundFieldObjectIn, letterIn, fontIn, pixelHeightIn):
        self.boundFieldObject = boundFieldObjectIn
        self.letterColor = ColorList.getRandomColorExcludingClosestToBackground(self.boundFieldObject.getColor())#ColorList.getRandomColor()[1]
        #print("letter color: " + str(self.letterColor))
        self.fontSize = int(pixelHeightIn*ObjectLetter.fontRatio)#this will convert the pixel height into the correct font. The ratio will have to be recalculated and changed if the font is changed
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

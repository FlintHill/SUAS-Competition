from SyntheticDataset.image_operations import *
from SyntheticDataset.color import *
import random
import os
from PIL import Image
import numpy

class Target(object):
    grassColor = (1,142,14,0)
    lowerLetterRadiusBound = 0.55
    upperLetterRadiusBound = 1
    possibleShapes = ["Triangle", "Square", "Rectangle", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Circle"]

    def __init__(self, shapeTypeIn, boundingBoxIn, rotationIn, colorIn, letterIn, data_path):
        self.data_path = data_path
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
        randomHeight = int((Target.lowerLetterRadiusBound + random.random()*(Target.upperLetterRadiusBound - Target.lowerLetterRadiusBound))*self.radius)

        #eventually replace the letter size with a method that gets a random height within reasonable bounds
        self.objectLetter = Letter(self, letter, os.path.join(self.data_path, "fonts/Blockletter.otf"), randomHeight)

    def __repr__(self):
        repString = "orientation: " + CompassAngler.getClosestCompassAngle(self.rotation) + "\n"
        repString += "shape: " + self.shapeType + "\n"
        repString += "background_color: " + ColorList.getClosestColorsName(self.color) + "\n"
        repString += "alphanumeric: " + self.objectLetter.getLetter() + "\n"
        repString += "alphanumeric_color: " + ColorList.getClosestColorsName(self.objectLetter.getColor())

        return repString

    def asNumpy(self):
        return numpy.asarray((CompassAngler.getClosestCompassAngle(self.rotation), self.shapeType, ColorList.getClosestColorsName(self.color), self.objectLetter.getLetter(), ColorList.getClosestColorsName(self.objectLetter.getColor())))

    def asDict(self):
        dictionary_representation = {
            "orientation" : CompassAngler.getClosestCompassAngle(self.rotation),
            "shape" : self.shapeType,
            "shape_color" : ColorList.getClosestColorsName(self.color),
            "letter" : self.objectLetter.getLetter(),
            "letter_color" : ColorList.getClosestColorsName(self.objectLetter.getColor()),
            "midpoint" : [self.getMidpointFromBounds().getX(), self.getMidpointFromBounds().getY()]
        }

        return dictionary_representation

    def setPolygon(self): #no trapezoid, cross, or star support yet.Rotations are clockwise for some reason in SimplePolygonMaker, so that's why self.rotation is negative on polygon creation.
        radius = self.getRadiusFromBounds()
        if self.shapeType in Target.possibleShapes:
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

    def get_letter(self):
        return self.objectLetter

    def fill(self, img, image):
        maskImg = self.polygon.getFilledMask(self.polygon.getBoundsWithMargin(Polygon.defaultMaskMargin), (0,0,0))
        margin = 10
        pasteMaskImg = Image.new('RGBA', (maskImg.size[0] + margin * 2, maskImg.size[1] + margin*2), (0,0,0,0))#this is created so that drop shadow has enough space to fuzz the edges
        pasteMaskImg.paste(maskImg, (margin, margin), maskImg)
        pasteMaskImg = GaussianBlur.getGaussianFilteredImgWithAlpha(pasteMaskImg, pasteMaskImg.load(), 5, 7)#this needs to be adjusted based on shape size, bigger shapes need bigger drop shadow.

        pasteShapeImg = self.polygon.getGradientFilledMask(self.polygon.getBoundsWithMargin(Polygon.defaultMaskMargin), self.color, self.grayGradient)#fillWithGradient(img, image, self.color, self.grayGradient)
        tempImg = Image.new('RGBA', pasteShapeImg.size, Target.grassColor)
        tempImg.paste(pasteShapeImg, (0,0), pasteShapeImg)
        pasteShapeImg = tempImg
        pasteShapeImg = GaussianBlur.getGaussianFilteredImg(pasteShapeImg, pasteShapeImg.load(), 3, .8)

        pasteMaskImg.paste(pasteShapeImg, (margin, margin), pasteShapeImg)
        newBounds = self.polygon.getBoundsWithMargin(Polygon.defaultMaskMargin + margin)
        img.paste(pasteMaskImg, (newBounds.getX(), newBounds.getY()), pasteMaskImg)
        self.pasteLetterImg(img)

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

    def get_bounding_rectangle(self):
        """
        Return this target's bounding rectangle
        """
        return self.bounds

    def getRadiusFromBounds(self):
        if self.bounds.getWidth() < self.bounds.getHeight():
            return self.bounds.getWidth()/2
        else:
            return self.bounds.getHeight()/2

    def getColor(self):
        return self.color

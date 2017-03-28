'''
Created on Jan 1, 2017

@author: phusisian
'''
import random
import numpy
from SyntheticDataset.image_operations import *
from SyntheticDataset.color import *
import string
import math
import os

class ImageGenerator(object):
    minWidth = 75
    minHeight = 75
    maxWidth = 200
    maxHeight = 200
    varianceTheta = math.pi/32.0
    blurKernelSize = 3
    blurStdDev = 2
    grassBlurStdDev = 2

    def __init__(self):
        self.polyPics = []
        self.grassLoader = ImageLoader("/Users/vtolpegin/github/SUAS-Competition/SyntheticDataset/Grass/")

    def fillPolyPics(self, numPics):
        for i in range(0, numPics):
            print("Generating image...")
            pic = self.grassLoader.getRandomImg().convert('RGBA')
            pic = GaussianBlur.getGaussianFilteredImg(pic, pic.load(), 3, ImageGenerator.grassBlurStdDev)
            pic = pic.convert('RGB')
            print("Finished applying Gaussian blur")
            fieldObject = self.getRandomlyGeneratedFieldObject(pic)
            self.applyFieldObjectToImg(fieldObject, pic)
            pic= ImageCropper.cropImgToRect(pic, fieldObject.getPolygon().getBoundsWithMargin(3)).convert('RGBA')
            pic = GaussianBlur.getGaussianFilteredImg(pic, pic.load(), ImageGenerator.blurKernelSize, ImageGenerator.blurStdDev)
            self.polyPics.append(PolyPic(pic, fieldObject))
            print("Filled polypic number: " + str(i))

    def showPolyPicImgs(self):
        for polyPic in self.polyPics:
            polyPic.getImg().show()

    def savePolyPicImgs(self, path):
        if not os.path.exists(path + "/Answers"):
            os.makedirs(path + "/Answers")
        if not os.path.exists(path+ "/Images"):
            os.makedirs(path + "/Images")
        for i in range(0, len(self.polyPics)):
            self.polyPics[i].getImg().save(path + "/Images/Generated Target " + str(i) + ".png")
            self.saveFieldObject(path, i)
            print("Saved polypic number: " + str(i))

    def saveFieldObject(self, path, index):
        fieldObject = self.polyPics[index].getFieldObject()
        details = fieldObject.asNumpy()
        numpy.save(path + "/Answers/Target " + str(index), details)

    def getRandomlyGeneratedFieldObject(self, backgroundImg):
        #backgroundImg = self.grassLoader.getRandomImg()
        shapeType = self.getRandomShapeType()
        bounds = self.getRandomBoundingBoxWithinImg(backgroundImg)
        #rotation = self.getRandomCompassAngle()
        color = ColorList.getRandomColor()
        letter = self.getRandomLetter()
        fieldObject = FieldObject(shapeType, bounds, self.getRandomTheta(), color, letter)
        return fieldObject
        #fieldObject.fill(backgroundImg, backgroundImg.load())

    def getRandomTheta(self):
        rand_base_theta = random.randint(0,8)*(math.pi/4.0)
        variance_theta = random.random()*ImageGenerator.varianceTheta - (ImageGenerator.varianceTheta/2.0)
        return rand_base_theta + variance_theta

    def applyFieldObjectToImg(self, fieldObject, imgIn):
        fieldObject.fill(imgIn, imgIn.load())
        return None

    def getRandomlyGeneratedPolyPic(self):
        backgroundImg = self.grassLoader.getRandomImg()
        fieldObject = self.getRandomlyGeneratedFieldObject(backgroundImg)

    def getRandomCompassAngle(self):
        return CompassAngler.getRandomCompassAngle()

    '''only returns a random uppercase letter'''
    def getRandomLetter(self):
        letters = dict(enumerate(string.ascii_uppercase, 0))
        randIndex = random.randint(0, len(letters) - 1)
        return letters[randIndex]

    def getRandomBoundingBoxWithinImg(self, img):
        '''randWidth and randHeight may need to be more intelligently generated.
        It's easier to have smaller shapes if both are randomized since the radius
        chosen by FieldObject is based off of the smallest side'''
        randWidth = random.randint(ImageGenerator.minWidth, ImageGenerator.maxWidth)
        randHeight = random.randint(ImageGenerator.minHeight, ImageGenerator.maxHeight)
        randX = random.randint(0, img.size[0]-randWidth-1)#not sure if I need to subtract one to prevent image out of bounds.
        randY = random.randint(0, img.size[1]-randHeight-1)#not sure if I need to subtract one to prevent image out of bounds.
        return Rectangle(randX, randY, randWidth, randHeight)
        #return Rectangle(200, 200, 100, 100)

    def getRandomShapeType(self):
        return FieldObject.possibleShapes[int(random.random() * len(FieldObject.possibleShapes))]

import random
import numpy
from SyntheticDataset.image_operations import *
from SyntheticDataset.color import *
import string
import math
import multiprocessing
import timeit
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

    def __init__(self, data_path, process_number=0):
        ColorList()

        self.polyPics = []
        self.data_path = data_path
        self.process_number = process_number
        self.grassLoader = ImageLoader(os.path.join(data_path, "grass"))
        self.starting_index = 0

    def fillPolyPics(self, numPics, starting_index):
        self.starting_index = starting_index
        for index in range(0, numPics + 1):
            start = timeit.default_timer()

            polygon_pic, field_object = self.generate_polygon()
            self.polyPics.append(PolyPic(polygon_pic, field_object))

            print("Finished generating image number", index, "in", (timeit.default_timer() - start), "seconds on process", self.process_number)

    def generate_polygon(self):
        """
        Generate a target
        """
        pic = self.grassLoader.getRandomImg().convert('RGBA')
        fieldObject = self.getRandomlyGeneratedFieldObject(pic)
        self.applyFieldObjectToImg(fieldObject, pic)
        pic = ImageCropper.cropImgToRect(pic, fieldObject.getPolygon().getBoundsWithMargin(3)).convert('RGBA')
        pic = GaussianBlur.getGaussianFilteredImg(pic, pic.load(), ImageGenerator.blurKernelSize, ImageGenerator.blurStdDev)

        return pic, fieldObject

    def showPolyPicImgs(self):
        for polyPic in self.polyPics:
            polyPic.getImg().show()

    def savePolyPicImgs(self, path):
        if not os.path.exists(path + "/Answers"):
            os.makedirs(path + "/Answers")
        if not os.path.exists(path+ "/Images"):
            os.makedirs(path + "/Images")
        for i in range(self.starting_index, len(self.polyPics) + self.starting_index):
            self.polyPics[i - self.starting_index].getImg().save(path + "/Images/Generated Target " + str(i) + ".png")
            self.saveFieldObject(path, i)
            print("Saved polypic number: " + str(i))

    def saveFieldObject(self, path, index):
        fieldObject = self.polyPics[index - self.starting_index].getFieldObject()
        details = fieldObject.asNumpy()
        numpy.save(path + "/Answers/Target " + str(index), details)

    def getRandomlyGeneratedFieldObject(self, backgroundImg):
        shapeType = self.getRandomShapeType()
        bounds = self.getRandomBoundingBoxWithinImg(backgroundImg)
        color = ColorList.getRandomColor()
        letter = self.getRandomLetter()

        fieldObject = FieldObject(shapeType, bounds, self.getRandomTheta(), color, letter, self.data_path)

        return fieldObject

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

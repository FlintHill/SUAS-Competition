import random
import numpy
from SyntheticDataset.image_operations import *
from SyntheticDataset.color import *
import string
import math
import multiprocessing
import timeit
import os
import json

class ImageGenerator(object):
    minWidth = 232
    minHeight = 232
    maxWidth = 232
    maxHeight = 232
    varianceTheta = math.pi/32.0
    blurKernelSize = 3
    blurStdDev = 2
    grassBlurStdDev = 2

    def __init__(self, data_path, process_number=0):
        ColorList()

        self.polyPics = []
        self.synthetic_images = []
        self.data_path = data_path
        self.process_number = process_number
        self.grassLoader = ImageLoader(os.path.join(data_path, "grass"))
        self.starting_index = 0

    def generate_synthetic_images(self, num_pics, num_targets_per_pic, starting_index):
        """
        Generate synthetic images (contain multiple targets per image)

        :param num_pics: The number of pictures to generate
        :type num_pics: int
        :param num_targets_per_pic: The number of targets to place on each picture
        :type num_targets_per_pic: int
        :param starting_index: The starting index of the pictures to generate.
            This is required for when multiprocessing is used to generate images
        :type starting_index: int
        """
        self.starting_index = starting_index
        for index in range(0, num_pics):
            start = timeit.default_timer()

            synthetic_pic = self.generate_synthetic_image(num_targets_per_pic)
            self.synthetic_images.append(synthetic_pic)

            print("Finished generating synthetic image number", index, "in", (timeit.default_timer() - start), "seconds on process", self.process_number)

    def generate_synthetic_image(self, num_targets):
        """
        Generates a single synthetic image

        :param num_targets: The number of targets to place on this image
        """
        pic = self.grassLoader.getRandomImg().convert('RGB')
        synthetic_image = SyntheticImage(num_targets, pic, self.data_path)

        return synthetic_image

    def fillPolyPics(self, numPics, starting_index):
        self.starting_index = starting_index
        for index in range(0, numPics):
            start = timeit.default_timer()

            polygon_pic, field_object = self.generate_polygon()
            self.polyPics.append(PolyPic(polygon_pic, field_object))

            print("Finished generating polygon number", index, "in", (timeit.default_timer() - start), "seconds on process", self.process_number)

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

    def save_synthetic_images(self, path):
        if not os.path.exists(path + "/Answers"):
            os.makedirs(path + "/Answers")
        if not os.path.exists(path+ "/Images"):
            os.makedirs(path + "/Images")
        for i in range(self.starting_index, len(self.synthetic_images) + self.starting_index):
            self.synthetic_images[i - self.starting_index].get_synthetic_image().save(path + "/Images/" + str(i) + ".png")
            self.save_synthetic_image(path, i)
            print("Saved synthetic image number: " + str(i))

    def savePolyPicImgs(self, path):
        if not os.path.exists(path + "/Answers"):
            os.makedirs(path + "/Answers")
        if not os.path.exists(path+ "/Images"):
            os.makedirs(path + "/Images")
        for i in range(self.starting_index, len(self.polyPics) + self.starting_index):
            self.polyPics[i - self.starting_index].getImg().save(path + "/Images/" + str(i) + ".png")
            self.saveFieldObject(path, i)
            print("Saved polypic number: " + str(i))

    def save_synthetic_image(self, path, index):
        """
        Save a synthetic image

        :param path: The path to save the synthetic image to
        :type path: str
        :param index: Image index in self.synthetic_images
        :type index: int
        """
        with open(path + "/Answers/Target " + str(index) + ".json", 'w+') as outfile:
            json.dump(self.synthetic_images[index - self.starting_index].asDict(), outfile, indent=4, sort_keys=True)

    def saveFieldObject(self, path, index):
        fieldObject = self.polyPics[index - self.starting_index].getFieldObject()
        details = fieldObject.asNumpy()
        numpy.save(path + "/Answers/" + str(index), details)

    def getRandomlyGeneratedFieldObject(self, backgroundImg):
        shapeType = self.getRandomShapeType()
        bounds = self.getRandomBoundingBoxWithinImg(backgroundImg)
        color = ColorList.getRandomColor()
        letter = self.getRandomLetter()

        fieldObject = Target(shapeType, bounds, self.getRandomTheta(), color, letter, self.data_path)

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
        return Target.possibleShapes[int(random.random() * len(Target.possibleShapes))]

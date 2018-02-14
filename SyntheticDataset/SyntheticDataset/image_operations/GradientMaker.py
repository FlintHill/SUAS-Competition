from PIL import Image
from random import random
from random import gauss

class GrayGradientMaker(object):

    def __init__(self, imgDimIn, stdDevIn):
        self.imgDim = imgDimIn
        self.stdDev = stdDevIn
        self.fillGradients()

    def fillGradients(self):
        self.gradients = [[0 for j in range(0, self.imgDim[1])]for i in range(0, self.imgDim[0])]#a reminder that I had the order of this flipped before, and that list comps work last index to first.
        for x in range(0, len(self.gradients)):
            for y in range(0, len(self.gradients[0])):
                self.gradients[x][y] = self.getRandomGradient()

    def getRandomGradient(self):
        return gauss(1, self.stdDev)

    def getGradients(self):
        return self.gradients

    def applyGradients(self, img, image):
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                '''surprisingly, values outside of 0-255 do not crash the method. I assume PIL sets them to zero if they are out of bounds
                This is temporary. Probably what would be best is if colors are going out of bounds, to shift the entire gradient down/up
                so that all values fall within 0-255. Otherwise very dark or very bright colors will have less variance because a lot of gradients
                wouldn't be properly applied.'''
                redVal = int(image[x,y][0] * self.gradients[x][y])
                greenVal = int(image[x,y][1] * self.gradients[x][y])
                blueVal = int(image[x,y][2] * self.gradients[x][y])
                image[x,y] = (redVal, greenVal, blueVal, image[x,y][3])
        return None

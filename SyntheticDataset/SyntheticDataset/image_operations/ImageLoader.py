import os
from PIL import Image
from random import random

'''loads images from a path, can return a random image, or can return all the images there.
Stuff like that.'''
class ImageLoader(object):

    def __init__(self, basePathIn):
        self.basePath = basePathIn
        self.dirContents = os.listdir(self.basePath)
        self.setImgPaths()

    def setImgPaths(self):
        self.imgPaths = ["" for i in range(0, len(self.dirContents))]
        for i in range(0, len(self.imgPaths)):
            self.imgPaths[i] = self.basePath + "/" + self.dirContents[i]

    def getRandomImg(self):
        return Image.open(self.getRandomImgPath())

    def getRandomImgPath(self):
        return self.imgPaths[int(random() * len(self.imgPaths))]

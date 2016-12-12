'''
Created on Dec 7, 2016

@author: phusisian
'''
from PIL import Image
from root.nested.Drawer import Drawer
from root.nested.Rectangle import Rectangle
class HarrisCorner:
    def __init__(self):
        self.testImg = Image.new("RGB", (100,100))
        self.testImage = self.testImg.load()
        rect = Rectangle()
        Drawer.fillRect(self.testImg, self.testImage,)
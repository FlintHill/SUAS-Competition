from SyntheticDataset.image_operations import *
import unittest
from PIL import Image
from images import *

class ImageBounderTestCase(unittest.TestCase):
    '''returns the bounds of a color in the image (with a margin so the pixel it finds at the edge is not excluded)'''

    def test_getBoundsOfColor(self):
        self.test_img = Image.open("tests/images/test_image1.jpg")
        self.test_image = self.test_img.load()
        self.test_color = [83,186,131]
        print (ImageBounder.getBoundsOfColor(self.test_img, self.test_image, self.test_color))
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img, self.test_image, self.test_color), Rectangle(1,1,1,1))



    def getBoundsOfColor(img, image, color):
        dim = img.size
        leftX = dim[0]-1
        rightX = 0
        upY = dim[1]-1
        lowY = 0
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if image[x,y] == color:
                    if x < leftX:
                        leftX = x
                    if x > rightX:
                        rightX = x
                    if y < upY:
                        upY = y
                    if y > lowY:
                        lowY = y
        return Rectangle(leftX-1, upY-1, (rightX+2) - (leftX-1), (lowY+2) - (upY-1))#numbers are being added/subtracted so that the bounds have a margin so that the pixels found aren't cropped out of image

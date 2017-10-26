"""
//Running Successfully

import unittest
from PIL import Image
from SyntheticDataset2.ImageOperations import *

class BoundedImageCropperTestCase(unittest.TestCase):

    def setUp(self):
        self.test_image1 = Image.open("tests/images/image1_test_image_bounder.png")
        self.test_image1_pixel = self.test_image1.load()

        self.test_image2 = Image.open("tests/images/image3_test_image_bounder.png")
        self.test_image2_pixel = self.test_image2.load()

        self.color1 = (255, 0, 0, 255)
        self.color2 = (0, 255, 0, 255)
        self.color3 = (0, 0, 255, 255)
        self.color4 = (255, 255, 255, 255)

        self.color5 = (0, 255, 255, 255)
        self.color6 = (252, 4, 163, 255)
        self.color7 = (254, 241, 2, 255)

    def test_crop_bounded_image(self):
        self.test_image3 = BoundedImageCropper.crop_bounded_image(self.test_image1, self.test_image1_pixel, self.color1)
        self.test_image4 = BoundedImageCropper.crop_bounded_image(self.test_image1, self.test_image1_pixel, self.color2)
        self.test_image5 = BoundedImageCropper.crop_bounded_image(self.test_image1, self.test_image1_pixel, self.color3)
        self.test_image6 = BoundedImageCropper.crop_bounded_image(self.test_image1, self.test_image1_pixel, self.color4)

        self.test_image7 = BoundedImageCropper.crop_bounded_image(self.test_image2, self.test_image2_pixel, self.color5)
        self.test_image8 = BoundedImageCropper.crop_bounded_image(self.test_image2, self.test_image2_pixel, self.color6)
        self.test_image9 = BoundedImageCropper.crop_bounded_image(self.test_image2, self.test_image2_pixel, self.color7)
        self.test_image10 = BoundedImageCropper.crop_bounded_image(self.test_image2, self.test_image2_pixel, self.color4)

        self.assertTrue(self.test_image3.load()[1, 1] == self.color1)
        self.assertTrue(self.test_image3.load()[self.test_image3.width/2, self.test_image3.height/2] == self.color1)
        self.assertTrue(self.test_image3.load()[self.test_image3.width-1, self.test_image3.height-1] == self.color1)

        self.assertTrue(self.test_image4.load()[1, 1] == self.color2)
        self.assertTrue(self.test_image4.load()[self.test_image4.width/2, self.test_image4.height/2] == self.color2)
        self.assertTrue(self.test_image4.load()[self.test_image4.width-1, self.test_image4.height-1] == self.color2)

        self.assertTrue(self.test_image5.load()[1, 1] == self.color3)
        self.assertTrue(self.test_image5.load()[self.test_image5.width/2, self.test_image5.height/2] == self.color3)
        self.assertTrue(self.test_image5.load()[self.test_image5.width-1, self.test_image5.height-1] == self.color3)

        self.assertTrue(self.test_image6.load()[1, 1] == self.color4)
        self.assertTrue(self.test_image6.load()[self.test_image6.width/2, self.test_image6.height/2] == self.color4)
        self.assertTrue(self.test_image6.load()[self.test_image6.width-1, self.test_image6.height-1] == self.color4)

        self.assertTrue(self.test_image7.load()[1, 1] == (0, 204, 1, 255))
        self.assertTrue(self.test_image7.load()[self.test_image7.width/2, self.test_image7.height/2] == self.color5)
        self.assertTrue(self.test_image7.load()[self.test_image7.width-1, self.test_image7.height-1] == (0, 51, 254, 255))

        self.assertTrue(self.test_image8.load()[1, 1] == (235, 28, 36, 255))
        self.assertTrue(self.test_image8.load()[self.test_image8.width/2, self.test_image8.height/2] == self.color6)
        self.assertTrue(self.test_image8.load()[self.test_image8.width-1, self.test_image8.height-1] == (0, 51, 254, 255))

        self.assertTrue(self.test_image9.load()[1, 1] == (235, 28, 36, 255))
        self.assertTrue(self.test_image9.load()[self.test_image9.width/2, self.test_image9.height/2] == self.color7)
        self.assertTrue(self.test_image9.load()[self.test_image9.width-1, self.test_image9.height-1] == self.color4)

        self.assertTrue(self.test_image10.load()[1, 1] == self.color7)
        self.assertTrue(self.test_image10.load()[self.test_image10.width/2, self.test_image10.height/2] == self.color4)
        self.assertTrue(self.test_image10.load()[self.test_image10.width-1, self.test_image10.height-1] == self.color5)

    def test_crop_bounded_image_inverse(self):
        self.test_image11 = BoundedImageCropper.crop_bounded_image_inverse(self.test_image1, self.test_image1_pixel, self.color1)
        self.test_image12 = BoundedImageCropper.crop_bounded_image_inverse(self.test_image1, self.test_image1_pixel, self.color2)
        self.test_image13 = BoundedImageCropper.crop_bounded_image_inverse(self.test_image1, self.test_image1_pixel, self.color3)
        self.test_image14 = BoundedImageCropper.crop_bounded_image_inverse(self.test_image1, self.test_image1_pixel, self.color4)

        self.test_image15 = BoundedImageCropper.crop_bounded_image_inverse(self.test_image2, self.test_image2_pixel, self.color5)
        self.test_image16 = BoundedImageCropper.crop_bounded_image_inverse(self.test_image2, self.test_image2_pixel, self.color6)
        self.test_image17 = BoundedImageCropper.crop_bounded_image_inverse(self.test_image2, self.test_image2_pixel, self.color7)
        self.test_image18 = BoundedImageCropper.crop_bounded_image_inverse(self.test_image2, self.test_image2_pixel, self.color4)

        self.assertTrue(self.test_image11.load()[1, 1] == self.color4)
        self.assertTrue(self.test_image11.load()[self.test_image11.width/2-1, self.test_image11.height/2-1] == self.color4)
        self.assertTrue(self.test_image11.load()[self.test_image11.width-1, self.test_image11.height-1] == self.color3)

        self.assertTrue(self.test_image12.load()[1, 1] == self.color4)
        self.assertTrue(self.test_image12.load()[self.test_image12.width/2+1, self.test_image12.height/2+1] == self.color3)
        self.assertTrue(self.test_image12.load()[self.test_image12.width-1, self.test_image12.height-1] == self.color3)

        self.assertTrue(self.test_image13.load()[1, 1] == self.color4)
        self.assertTrue(self.test_image13.load()[self.test_image13.width/2-1, self.test_image13.height/2+1] == self.color2)
        self.assertTrue(self.test_image13.load()[self.test_image13.width-1, self.test_image13.height-1] == self.color3)

        self.assertTrue(self.test_image14.load()[1, 1] == self.color4)
        self.assertTrue(self.test_image14.load()[self.test_image14.width/2+1, self.test_image14.height/2-1] == self.color1)
        self.assertTrue(self.test_image14.load()[self.test_image14.width-1, self.test_image14.height-1] == self.color3)

        self.assertTrue(self.test_image15.load()[self.test_image15.width/2, self.test_image15.height/2] == self.color4)

        self.assertTrue(self.test_image16.load()[self.test_image16.width/2, self.test_image16.height/2] == self.color4)

        self.assertTrue(self.test_image17.load()[self.test_image17.width/2, self.test_image17.height/2] == self.color4)

        self.assertTrue(self.test_image18.load()[self.test_image18.width/2, self.test_image18.height/2] == self.color4)
"""

from SyntheticDataset.image_operations import *
import unittest
from PIL import Image

class ImageBounderTestCase(unittest.TestCase):


    def test_getBoundsOfColor(self):
        self.test_img1 = Image.open("images/test_image2.png")
        self.test_image1 = self.test_img1.load()
        self.test_color1 = (255,255,255,255)
        self.test_img2 = self.test_img1.copy()
        self.test_image2 = self.test_img2.load()

        print (ImageBounder.getBoundsOfColor(self.test_img1, self.test_image1, self.test_color1))

        #self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img1, self.test_image1, self.test_color1), Rectangle(-1,-1,322,242))
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img1, self.test_image1, self.test_color1).getX(), -1)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img1, self.test_image1, self.test_color1).getY(), -1)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img1, self.test_image1, self.test_color1).getWidth(), 320)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img1, self.test_image1, self.test_color1).getHeight(), 240)

        self.test_resultant1 = self.test_img1.crop((-1, -1, 320, 240))
        self.test_resultant1.show()

        self.test_color2 = (255,0,0,255)

        print (ImageBounder.getBoundsOfColor(self.test_img2, self.test_image2, self.test_color2))

        #self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img2, self.test_image1, self.test_color2), Rectangle(319,-1,322,242))
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img2, self.test_image2, self.test_color2).getX(), 319)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img2, self.test_image2, self.test_color2).getY(), -1)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img2, self.test_image2, self.test_color2).getWidth(), 640)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img2, self.test_image2, self.test_color2).getHeight(), 240)

        self.test_resultant2 = self.test_img2.crop((319, -1, 640, 240))
        self.test_resultant2.show()

        self.test_img3 = Image.open("images/test_image1.jpg")
        self.test_image3 = self.test_img3.load()
        self.test_color3 = (9,81,105)
        self.test_img4 = self.test_img3.copy()
        self.test_image4 = self.test_img4.load()

        print (ImageBounder.getBoundsOfColor(self.test_img3, self.test_image3, self.test_color3))

        #self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img3, self.test_image2, self.test_color3), Rectangle(-1,-1,322,242))
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img3, self.test_image3, self.test_color3).getX(), 111)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img3, self.test_image3, self.test_color3).getY(), -1)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img3, self.test_image3, self.test_color3).getWidth(), 208)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img3, self.test_image3, self.test_color3).getHeight(), 416)

        self.test_resultant3 = self.test_img3.crop((111, -1, 208, 416))
        self.test_resultant3.show()

        self.test_color4 = (83,186,131)

        print (ImageBounder.getBoundsOfColor(self.test_img4, self.test_image4, self.test_color4))

        #self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img4, self.test_image2, self.test_color4), Rectangle(319,-1,322,242))
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img4, self.test_image4, self.test_color4).getX(), 335)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img4, self.test_image4, self.test_color4).getY(), -1)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img4, self.test_image4, self.test_color4).getWidth(), 432)
        self.assertEqual(ImageBounder.getBoundsOfColor(self.test_img4, self.test_image4, self.test_color4).getHeight(), 416)

        self.test_resultant4 = self.test_img4.crop((335, -1, 432, 416))
        self.test_resultant4.show()

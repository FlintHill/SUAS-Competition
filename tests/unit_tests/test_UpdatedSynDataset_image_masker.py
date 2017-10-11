import unittest
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *
from PIL import Image

class ImageMaskerTestCase(unittest.TestCase):

    def setUp(self):
        self.test_image1 = Image.open("tests/images/image1_test_image_bounder.png")
        self.test_image2 = Image.open("tests/images/image3_test_image_bounder.png")

        self.test_image1a = self.test_image1.copy()
        self.test_image1b = self.test_image1.copy()
        self.test_image1c = self.test_image1.copy()
        self.test_image1d = self.test_image1.copy()

        self.test_image3 = ImageMasker.mask_image(self.test_image1a, self.test_image1a.load(), (255, 255, 255, 255), (255, 0, 0, 255))
        self.test_image4 = ImageMasker.mask_image(self.test_image1b, self.test_image1b.load(), (255, 0, 0, 255), (0, 255, 0, 255))
        self.test_image5 = ImageMasker.mask_image(self.test_image1c, self.test_image1c.load(), (0, 255, 0, 255), (0, 0, 255, 255))
        self.test_image6 = ImageMasker.mask_image(self.test_image1d, self.test_image1d.load(), (0, 0, 255, 255), (255, 255, 255, 255))

        self.test_image2a = self.test_image2.copy()
        self.test_image2b = self.test_image2.copy()
        self.test_image2c = self.test_image2.copy()
        self.test_image2d = self.test_image2.copy()

        self.test_image7 = ImageMasker.mask_image(self.test_image2a, self.test_image2a.load(), (0, 255, 255, 255), (0, 51, 254, 255))
        self.test_image8 = ImageMasker.mask_image(self.test_image2b, self.test_image2b.load(), (252, 4, 163, 255), (235, 28, 36, 255))
        self.test_image9 = ImageMasker.mask_image(self.test_image2c, self.test_image2c.load(), (254, 241, 2, 255), (0, 204, 1, 255))
        self.test_image10 = ImageMasker.mask_image(self.test_image2d, self.test_image2d.load(), (255, 255, 255, 255), (0, 0, 0, 255))

    def test_mask_image(self):
        self.assertTrue(self.test_image3.load()[1, 1] == (255, 255, 255, 255))
        self.assertTrue(self.test_image3.load()[self.test_image3.width/2-1, self.test_image3.height/2-1] == (255, 255, 255, 255))
        self.assertTrue(self.test_image3.load()[self.test_image3.width/2+1, self.test_image3.height/2+1] == (255, 255, 255, 255))
        self.assertTrue(self.test_image3.load()[self.test_image3.width/2-1, self.test_image3.height/2+1] == (255, 255, 255, 255))
        self.assertTrue(self.test_image3.load()[self.test_image3.width/2+1, self.test_image3.height/2-1] == (255, 0, 0, 255))
        self.assertTrue(self.test_image3.load()[self.test_image3.width-1, self.test_image3.height-1] == (255, 255 ,255 ,255))

        self.assertTrue(self.test_image4.load()[1, 1] == (255, 0, 0, 255))
        self.assertTrue(self.test_image4.load()[self.test_image4.width/2-1, self.test_image4.height/2-1] == (255, 0, 0, 255))
        self.assertTrue(self.test_image4.load()[self.test_image4.width/2+1, self.test_image4.height/2+1] == (255, 0, 0, 255))
        self.assertTrue(self.test_image4.load()[self.test_image4.width/2-1, self.test_image4.height/2+1] == (0, 255, 0, 255))
        self.assertTrue(self.test_image4.load()[self.test_image4.width/2+1, self.test_image4.height/2-1] == (255, 0, 0, 255))
        self.assertTrue(self.test_image4.load()[self.test_image4.width-1, self.test_image4.height-1] == (255, 0, 0, 255))

        self.assertTrue(self.test_image5.load()[1, 1] == (0, 255, 0, 255))
        self.assertTrue(self.test_image5.load()[self.test_image5.width/2-1, self.test_image5.height/2-1] == (0, 255, 0, 255))
        self.assertTrue(self.test_image5.load()[self.test_image5.width/2+1, self.test_image5.height/2+1] == (0, 0, 255, 255))
        self.assertTrue(self.test_image5.load()[self.test_image5.width/2-1, self.test_image5.height/2+1] == (0, 255, 0, 255))
        self.assertTrue(self.test_image5.load()[self.test_image5.width/2+1, self.test_image5.height/2-1] == (0, 255, 0, 255))
        self.assertTrue(self.test_image5.load()[self.test_image5.width-1, self.test_image5.height-1] == (0, 0, 255, 255))

        self.assertTrue(self.test_image6.load()[1, 1] == (255, 255, 255, 255))
        self.assertTrue(self.test_image6.load()[self.test_image6.width/2-1, self.test_image6.height/2-1] == (255, 255, 255, 255))
        self.assertTrue(self.test_image6.load()[self.test_image6.width/2+1, self.test_image6.height/2+1] == (0, 0, 255, 255))
        self.assertTrue(self.test_image6.load()[self.test_image6.width/2-1, self.test_image6.height/2+1] == (0, 0, 255, 255))
        self.assertTrue(self.test_image6.load()[self.test_image6.width/2+1, self.test_image6.height/2-1] == (0, 0, 255, 255))
        self.assertTrue(self.test_image6.load()[self.test_image6.width-1, self.test_image6.height-1] == (0, 0, 255, 255))

        self.assertTrue(self.test_image7.load()[200, 100] == (0, 255, 255, 255))
        self.assertTrue(self.test_image7.load()[100, 300] == (0, 255, 255, 255))
        self.assertTrue(self.test_image7.load()[300, 300] == (0, 51, 254, 255))

        self.assertTrue(self.test_image8.load()[200, 100] == (235, 28, 36, 255))
        self.assertTrue(self.test_image8.load()[100, 300] == (252, 4, 163, 255))
        self.assertTrue(self.test_image8.load()[300, 300] == (252, 4, 163, 255))

        self.assertTrue(self.test_image9.load()[200, 100] == (254, 241, 2, 255))
        self.assertTrue(self.test_image9.load()[100, 300] == (0, 204, 1, 255))
        self.assertTrue(self.test_image9.load()[300, 300] == (254, 241, 2, 255))

        self.assertTrue(self.test_image10.load()[200, 100] == (255, 255, 255, 255))
        self.assertTrue(self.test_image10.load()[100, 300] == (255, 255, 255, 255))
        self.assertTrue(self.test_image10.load()[300, 300] == (255, 255, 255, 255))

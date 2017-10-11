import unittest
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

class ImageExtenderTestCase(unittest.TestCase):

    def setUp(self):
        self.font_type = "UpdatedSyntheticDataset/data/fonts/Blockletter.otf"

        self.test_image1 = SpecifiedLetterGenerator("I", self.font_type, 200, (255, 255, 0, 255)).generate_specified_letter()
        self.test_image2 = SpecifiedLetterGenerator("N", self.font_type, 400, (255, 0, 255, 255)).generate_specified_letter()
        self.test_image3 = SpecifiedLetterGenerator("F", self.font_type, 600, (0, 255, 255, 255)).generate_specified_letter()
        self.test_image4 = SpecifiedLetterGenerator("Z", self.font_type, 800, (233, 233, 233, 255)).generate_specified_letter()
        self.test_image5 = SpecifiedLetterGenerator("Y", self.font_type, 1000, (123, 123, 123, 255)).generate_specified_letter()

        self.test_image6 = ImageExtender.extend_image(self.test_image1, 10, 0)
        self.test_image7 = ImageExtender.extend_image(self.test_image2, 0, 10)
        self.test_image8 = ImageExtender.extend_image(self.test_image3, 100, 100)
        self.test_image9 = ImageExtender.extend_image(self.test_image4, 1, 100)
        self.test_image10 = ImageExtender.extend_image(self.test_image5, 100, 1)

    def test_extend_image(self):
        self.assertTrue(self.test_image1.width + 20 == self.test_image6.width)
        self.assertTrue(self.test_image1.height == self.test_image6.height)

        self.assertTrue(self.test_image2.width == self.test_image7.width)
        self.assertTrue(self.test_image2.height + 20 == self.test_image7.height)

        self.assertTrue(self.test_image3.width + 200 == self.test_image8.width)
        self.assertTrue(self.test_image3.height + 200 == self.test_image8.height)

        self.assertTrue(self.test_image4.width + 2 == self.test_image9.width)
        self.assertTrue(self.test_image4.height + 200 == self.test_image9.height)

        self.assertTrue(self.test_image5.width + 200 == self.test_image10.width)
        self.assertTrue(self.test_image5.height + 2 == self.test_image10.height)

"""
//Running Successfully

import unittest
from PIL import Image
from SyntheticDataset2.ElementsCreator import *

class RawImageGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.test_image1 = RawImageGenerator.generate_raw_image(100, 100, (233, 233, 233, 255))
        self.test_image2 = RawImageGenerator.generate_raw_image(1, 999, (66, 66, 66, 255))
        self.test_image3 = RawImageGenerator.generate_raw_image(999, 1, (66, 233, 233, 255))
        self.test_image4 = RawImageGenerator.generate_raw_image(233, 666, (233, 66, 233, 255))
        self.test_image5 = RawImageGenerator.generate_raw_image(666, 233, (233, 233, 66, 255))

    def test_generate_raw_image(self):
        self.assertTrue(self.test_image1.width == 100)
        self.assertTrue(self.test_image1.height == 100)
        self.assertTrue(self.test_image1.load()[0, 0] == (233, 233, 233, 255))

        self.assertTrue(self.test_image2.width == 1)
        self.assertTrue(self.test_image2.height == 999)
        self.assertTrue(self.test_image2.load()[0, 0] == (66, 66, 66, 255))

        self.assertTrue(self.test_image3.width == 999)
        self.assertTrue(self.test_image3.height == 1)
        self.assertTrue(self.test_image3.load()[0, 0] == (66, 233, 233, 255))

        self.assertTrue(self.test_image4.width == 233)
        self.assertTrue(self.test_image4.height == 666)
        self.assertTrue(self.test_image4.load()[0, 0] == (233, 66, 233, 255))

        self.assertTrue(self.test_image5.width == 666)
        self.assertTrue(self.test_image5.height == 233)
        self.assertTrue(self.test_image5.load()[0, 0] == (233, 233, 66, 255))
"""

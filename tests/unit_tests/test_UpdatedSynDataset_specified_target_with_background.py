"""
Running Successfully

import unittest
import math
from PIL import Image
from SyntheticDataset2.ImageCreator.specified_target_with_background import SpecifiedTargetWithBackground

class SpecifiedTargetWithBackgroundTestCase(unittest.TestCase):

    def setUp(self):
        self.path_to_background = "tests/images/competition_grass_1.JPG"
        self.test_image1 = SpecifiedTargetWithBackground("circle", "?", "A", (255, 255, 255, 255), (255, 0, 0, 255), 0).create_specified_target_with_background()
        self.test_image2 = SpecifiedTargetWithBackground("semicircle", "E", "E", (0, 255, 0, 255), (0, 0, 255, 255), 45).create_specified_target_with_background()
        self.test_image3 = SpecifiedTargetWithBackground("cross", "D", "I", (255, 255, 0, 255), (255, 0, 255, 255), 90).create_specified_target_with_background()
        self.test_image4 = SpecifiedTargetWithBackground("heptagon", "S", "O", (0, 255, 255, 255), (0, 0, 0, 255), 135).create_specified_target_with_background()
        self.test_image5 = SpecifiedTargetWithBackground("star", "N", "U", (66, 66, 66, 255), (233, 233, 233, 255), 180).create_specified_target_with_background()
        '''
        Settings:
        PPSI = 10
        SINGLE_TARGET_SIZE_IN_INCHES = 24
        SINGLE_TARGET_PROPORTIONALITY = 2.5
        PIXELIZATION_LEVEL = 0
        NOISE_LEVEL = 0
        '''

    def test_create_specified_target_with_specified_background(self):
        self.assertTrue(abs(max(self.test_image1.width, self.test_image1.height) - 260) < 3)
        self.assertTrue(self.test_image1.load()[self.test_image1.width/2, self.test_image1.height/2] == (255, 255, 255))

        self.assertTrue(abs(max(self.test_image2.width, self.test_image2.height) - 260) < 3)
        self.assertTrue(self.test_image2.load()[self.test_image2.width/2, self.test_image2.height/2] == (0, 255, 0))

        self.assertTrue(abs(max(self.test_image2.width, self.test_image2.height) - 260) < 3)
        self.assertTrue(self.test_image3.load()[self.test_image3.width/2, self.test_image3.height/2] == (255, 0, 255))

        self.assertTrue(abs(max(self.test_image2.width, self.test_image2.height) - 260) < 3)
        self.assertTrue(self.test_image4.load()[self.test_image4.width/2, self.test_image4.height/2] == (0, 255, 255))

        self.assertTrue(abs(max(self.test_image2.width, self.test_image2.height) - 260) < 3)
        self.assertTrue(self.test_image5.load()[self.test_image5.width/2, self.test_image5.height/2] == (66, 66, 66))
"""

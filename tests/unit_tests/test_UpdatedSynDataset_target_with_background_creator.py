import unittest
import math
from PIL import Image
from SyntheticDataset2.ImageCreator.target_with_background_creator import TargetWithBackgroundCreator

class TargetWithBackgroundCreatorTestCase(unittest.TestCase):

    def setUp(self):
        self.path_to_background = "tests/images/competition_grass_1.JPG"
        self.test_image1 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("circle", "?", "A", 300, 1.5, (255, 255, 255, 255), (255, 0, 0, 255), self.path_to_background, 0)
        self.test_image2 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("half_circle", "E", "E", 400, 1.75, (0, 255, 0, 255), (0, 0, 255, 255), self.path_to_background, 45)
        self.test_image3 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("cross", "D", "I", 500, 2.0, (255, 255, 0, 255), (255, 0, 255, 255), self.path_to_background, 90)
        self.test_image4 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("heptagon", "S", "O", 600, 2.25, (0, 255, 255, 255), (0, 0, 0, 255), self.path_to_background, 135)
        self.test_image5 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("star", "N", "U", 700, 2.5, (66, 66, 66, 255), (233, 233, 233, 255), self.path_to_background, 180)

    def test_create_specified_target_with_specified_background(self):
        self.assertTrue(abs(self.test_image1.width - (300 + 20)) < 3)
        self.assertTrue(abs(self.test_image1.height - (300 + 20)) < 3)
        self.assertTrue(self.test_image1.load()[1, 1] != (255, 255, 255))
        self.assertTrue(self.test_image1.load()[self.test_image1.width-1, self.test_image1.height-1] != (255, 255, 255))
        self.assertTrue(self.test_image1.load()[self.test_image1.width/2, self.test_image1.height/2] == (255, 255, 255))

        self.assertTrue(abs(self.test_image2.width - self.test_image2.height) < 3)
        self.assertTrue(self.test_image2.load()[1, 1] != (0, 255, 0))
        self.assertTrue(self.test_image2.load()[self.test_image2.width-1, self.test_image2.height-1] != (0, 255, 0))
        self.assertTrue(self.test_image2.load()[self.test_image2.width/2, self.test_image2.height/2] == (0, 255, 0))

        self.assertTrue(abs(self.test_image3.width - (2000 * math.sqrt(2) / 3 + 20)) < 3)
        self.assertTrue(abs(self.test_image3.height - (2000 * math.sqrt(2) / 3 + 20)) < 3)
        self.assertTrue(self.test_image3.load()[1, 1] != (255, 255, 0))
        self.assertTrue(self.test_image3.load()[self.test_image3.width-1, self.test_image3.height-1] != (255, 255, 0))
        self.assertTrue(self.test_image3.load()[self.test_image3.width/2, self.test_image3.height/2] == (255, 0, 255))

        self.assertTrue(self.test_image4.load()[1, 1] != (0, 255, 255))
        self.assertTrue(self.test_image4.load()[self.test_image4.width-1, self.test_image4.height-1] != (0, 255, 255))
        self.assertTrue(self.test_image4.load()[self.test_image4.width/2, self.test_image4.height/2] == (0, 255, 255))

        self.assertTrue(abs(self.test_image5.width - (2 * 700 / 1.1 * math.sin(math.radians(72)) + 20)) < 3)
        self.assertTrue(abs(self.test_image5.height - ((700 / 1.1) + (700 / 1.1 * math.cos(math.radians(36))) + 20)) < 3)
        self.assertTrue(self.test_image5.load()[1, 1] != (66, 66, 66))
        self.assertTrue(self.test_image5.load()[self.test_image5.width-1, self.test_image5.height-1] != (66, 66, 66))
        self.assertTrue(self.test_image5.load()[self.test_image5.width/2, self.test_image5.height/2] == (66, 66, 66))

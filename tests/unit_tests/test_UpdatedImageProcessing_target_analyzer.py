import unittest
from PIL import Image
from UpdatedImageProcessing.TargetDetection import *

class TargetAnalyzerTestCase(unittest.TestCase):

    def setUp(self):
        self.test_image1 = Image.open("tests/images/image1_test_image_bounder.png")

    def test_find_target_average_color(self):
        self.target_average_color1 = TargetAnalyzer.find_target_average_color(self.test_image1, (140, 100, 40, 40))
        self.target_average_color2 = TargetAnalyzer.find_target_average_color(self.test_image1, (460, 100, 40, 40))
        self.target_average_color3 = TargetAnalyzer.find_target_average_color(self.test_image1, (300, 340, 40, 40))
        self.target_average_color4 = TargetAnalyzer.find_target_average_color(self.test_image1, (460, 220, 40, 40))

        self.assertTrue(abs(self.target_average_color1[0] - 255) < 5)
        self.assertTrue(abs(self.target_average_color1[1] - 255) < 5)
        self.assertTrue(abs(self.target_average_color1[2] - 255) < 5)

        self.assertTrue(abs(self.target_average_color2[0] - 255) < 5)
        self.assertTrue(abs(self.target_average_color2[1] - 0) < 5)
        self.assertTrue(abs(self.target_average_color2[2] - 0) < 5)

        self.assertTrue(abs(self.target_average_color3[0] - 0) < 5)
        self.assertTrue(abs(self.target_average_color3[1] - 102) < 5)
        self.assertTrue(abs(self.target_average_color3[2] - 153) < 5)

        self.assertTrue(abs(self.target_average_color4[0] - 102) < 5)
        self.assertTrue(abs(self.target_average_color4[1] - 0) < 5)
        self.assertTrue(abs(self.target_average_color4[2] - 153) < 5)

    def test_find_surrounding_average_color(self):
        self.surrounding_average_color1 = TargetAnalyzer.find_surrounding_average_color(self.test_image1, (140, 100, 40, 40))
        self.surrounding_average_color2 = TargetAnalyzer.find_surrounding_average_color(self.test_image1, (460, 100, 40, 40))
        self.surrounding_average_color3 = TargetAnalyzer.find_surrounding_average_color(self.test_image1, (300, 340, 40, 40))
        self.surrounding_average_color4 = TargetAnalyzer.find_surrounding_average_color(self.test_image1, (460, 220, 40, 40))

        self.assertTrue(abs(self.surrounding_average_color1[0] - 255) < 5)
        self.assertTrue(abs(self.surrounding_average_color1[1] - 255) < 5)
        self.assertTrue(abs(self.surrounding_average_color1[2] - 255) < 5)

        self.assertTrue(abs(self.surrounding_average_color2[0] - 255) < 5)
        self.assertTrue(abs(self.surrounding_average_color2[1] - 0) < 5)
        self.assertTrue(abs(self.surrounding_average_color2[2] - 0) < 5)

        self.assertTrue(abs(self.surrounding_average_color3[0] - 0) < 5)
        self.assertTrue(abs(self.surrounding_average_color3[1] - 95) < 5)
        self.assertTrue(abs(self.surrounding_average_color3[2] - 159) < 5)

        self.assertTrue(abs(self.surrounding_average_color4[0] - 95) < 5)
        self.assertTrue(abs(self.surrounding_average_color4[1] - 0) < 5)
        self.assertTrue(abs(self.surrounding_average_color4[2] - 159) < 5)

    def test_find_rim_average_color(self):
        self.rim_average_color = TargetAnalyzer.find_rim_average_color(self.test_image1)

        self.assertTrue(abs(self.rim_average_color[0] - 127) < 5)
        self.assertTrue(abs(self.rim_average_color[1] - 127) < 5)
        self.assertTrue(abs(self.rim_average_color[2] - 127) < 5)

    def test_find_average_corner_color(self):
        self.average_corner_color = TargetAnalyzer.find_average_corner_color(self.test_image1)

        self.assertTrue(abs(self.average_corner_color[0] - 127) < 5)
        self.assertTrue(abs(self.average_corner_color[1] - 127) < 5)
        self.assertTrue(abs(self.average_corner_color[2] - 127) < 5)

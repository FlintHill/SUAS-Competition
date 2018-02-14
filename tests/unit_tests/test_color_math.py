from SyntheticDataset import ColorMath
import unittest
from math import sqrt

class ColorMathTestCase(unittest.TestCase):

    def test_get_magnitude_between_colors(self):
        colora = [0,0,220]
        colorb = [10,80,225]
        magnitude = ColorMath.getMagnitudeBetweenColors(colora, colorb)
        self.assertEqual(sqrt(6525), magnitude)

    def test_get_most_similar_color(self):
        test_color = [204,0,0]
        test_red = [255,0,0]
        test_blue = [0,0,255]
        test_yellow = [255,255,0]
        test_green = [0,255,0]
        test_purple = [255,0,255]
        test_colors = [test_red,test_blue,test_yellow,test_green,test_purple]
        similarColor = ColorMath.getMostSimilarColor(test_colors, test_color)
        self.assertEqual(test_red, similarColor)

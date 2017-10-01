from SyntheticDataset import ColorMath
import unittest
from math import sqrt

class TestColorMath(unittest.TestCase):

    def test_get_magnitude_between_colors(self):
        colorA = [0,0,220]
        colorB = [10,80,225]
        magnitude = ColorMath.getMagnitudeBetweenColors(colorA, colorB)
        self.assertEqual(sqrt(6525), magnitude)

    def test_get_most_similar_color(self):
        color = [204,0,0]
        red = [255,0,0]
        blue = [0,0,255]
        yellow = [255,255,0]
        green = [0,255,0]
        purple = [255,0,255]
        colors = [red,blue,yellow,green,purple]
        similarColor = ColorMath.getMostSimilarColor(colors, color)
        self.assertEqual(red, similarColor)

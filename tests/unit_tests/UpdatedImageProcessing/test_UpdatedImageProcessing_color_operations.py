import unittest
from PIL import Image
from UpdatedImageProcessing.TargetDetection import *

class ColorOperationsTestCase(unittest.TestCase):

    def setUp(self):
        self.color1 = (255, 0, 0, 255)
        self.color2 = (0, 255, 0, 255)
        self.color3 = (0, 0, 255, 255)
        self.color4 = (255, 255, 255, 255)
        self.color5 = (0, 255, 255, 255)
        self.color6 = (252, 4, 163, 255)
        self.color7 = (254, 241, 2, 255)
        self.color8 = (0, 0, 0, 255)

        self.test_image1 = Image.open("tests/images/image1_test_image_bounder.png")
        self.test_image2 = Image.open("tests/images/image3_test_image_bounder.png")

    def test_find_distance(self):
        self.distance1 = ColorOperations.find_distance(self.color1, self.color2)
        self.distance2 = ColorOperations.find_distance(self.color3, self.color4)
        self.distance3 = ColorOperations.find_distance(self.color5, self.color6)
        self.distance4 = ColorOperations.find_distance(self.color7, self.color8)

        self.assertTrue(abs(self.distance1 - 360) < 5)
        self.assertTrue(abs(self.distance2 - 360) < 5)
        self.assertTrue(abs(self.distance3 - 365) < 5)
        self.assertTrue(abs(self.distance4 - 350) < 5)

    def test_find_percentage_difference(self):
        self.difference1 = ColorOperations.find_percentage_difference(self.color1, self.color2)
        self.difference2 = ColorOperations.find_percentage_difference(self.color3, self.color4)
        self.difference3 = ColorOperations.find_percentage_difference(self.color5, self.color6)
        self.difference4 = ColorOperations.find_percentage_difference(self.color7, self.color8)

        self.assertTrue(abs(self.difference1 - 80) < 5)
        self.assertTrue(abs(self.difference2 - 80) < 5)
        self.assertTrue(abs(self.difference3 - 80) < 5)
        self.assertTrue(abs(self.difference4 - 80) < 5)

    def test_find_boundary_of_color(self):
        self.boundary1 = ColorOperations.find_boundary_of_color(self.test_image1, self.color1, 0)
        self.boundary2 = ColorOperations.find_boundary_of_color(self.test_image1, self.color2, 5)
        self.boundary3 = ColorOperations.find_boundary_of_color(self.test_image1, self.color7, 10)
        self.boundary4 = ColorOperations.find_boundary_of_color(self.test_image1, self.color8, 15)

        self.boundary5 = ColorOperations.find_boundary_of_color(self.test_image2, self.color3, 0)
        self.boundary6 = ColorOperations.find_boundary_of_color(self.test_image2, self.color4, 5)
        self.boundary7 = ColorOperations.find_boundary_of_color(self.test_image2, self.color5, 10)
        self.boundary8 = ColorOperations.find_boundary_of_color(self.test_image2, self.color6, 15)

        self.assertTrue(abs(self.boundary1[0] - 320) < 5)
        self.assertTrue(abs(self.boundary1[1] - 0) < 5)
        self.assertTrue(abs(self.boundary1[2] - 640) < 5)
        self.assertTrue(abs(self.boundary1[3] - 240) < 5)

        self.assertTrue(abs(self.boundary2[0] - 0) < 5)
        self.assertTrue(abs(self.boundary2[1] - 235) < 5)
        self.assertTrue(abs(self.boundary2[2] - 325) < 5)
        self.assertTrue(abs(self.boundary2[3] - 480) < 5)

        self.assertTrue(self.boundary3 == -1)

        self.assertTrue(self.boundary4 == -1)

        self.assertTrue(self.boundary5 == -1)

        self.assertTrue(abs(self.boundary6[0] - 155) <= 5)
        self.assertTrue(abs(self.boundary6[1] - 175) <= 5)
        self.assertTrue(abs(self.boundary6[2] - 245) <= 5)
        self.assertTrue(abs(self.boundary6[3] - 255) <= 5)

        self.assertTrue(abs(self.boundary7[0] - 145) <= 5)
        self.assertTrue(abs(self.boundary7[1] - 230) <= 5)
        self.assertTrue(abs(self.boundary7[2] - 255) <= 5)
        self.assertTrue(abs(self.boundary7[3] - 380) <= 5)

        self.assertTrue(abs(self.boundary8[0] - 185) <= 5)
        self.assertTrue(abs(self.boundary8[1] - 135) <= 5)
        self.assertTrue(abs(self.boundary8[2] - 340) <= 5)
        self.assertTrue(abs(self.boundary8[3] - 255) <= 5)

import unittest
import os
from PIL import Image
from SUASSystem.utils import crop_target

class SUASSystemUtilsDataFunctionsTestCase(unittest.TestCase):

    def test_crop_image(self):
        """
        Test the crop image method.
        """
        input_image_path = "tests/images/image2_test_image_bounder.jpg"
        output_crop_image_path = "tests/images/test_crop.jpg"
        top_left_coords = [250.0, 200.0]
        bottom_right_coords = [350.0, 300.0]

        crop_target(input_image_path, output_crop_image_path, top_left_coords, bottom_right_coords)

        saved_crop = Image.open(output_crop_image_path).load()
        input_image = Image.open(input_image_path).load()

        self.assertEqual(saved_crop[0, 0], input_image[250, 200])
        self.assertEqual(saved_crop[1, 1], input_image[251, 201])
        self.assertEqual(saved_crop[50, 50], input_image[300, 250])
        self.assertEqual(saved_crop[99, 99], input_image[349, 299])

        os.remove("tests/images/test_crop.jpg")

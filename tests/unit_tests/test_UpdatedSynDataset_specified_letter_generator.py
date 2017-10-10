from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SyntheticDataset2.ImageOperations import *
from SyntheticDataset2.ElementsCreator import *
import random
import unittest

class SpecifiedLetterGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.test_letter_input1 = "I"
        self.test_letter_input2 = "N"
        self.test_letter_input3 = "F"
        self.test_letter_input4 = "Z"
        self.test_letter_input5 = "Y"
        self.test_letter_input6 = "I"
        self.test_letter_input7 = "N"
        self.test_letter_input8 = "F"
        self.test_letter_input9 = "Z"
        self.test_letter_input10 = "Y"
        self.test_letter_input_x = "X"

        self.font_type = "UpdatedSyntheticDataset/data/fonts/Blockletter.otf"

        self.test_font_size1 = 121
        self.test_font_size2 = 232
        self.test_font_size3 = 343
        self.test_font_size4 = 454
        self.test_font_size5 = 565
        self.test_font_size6 = 676
        self.test_font_size7 = 787
        self.test_font_size8 = 898
        self.test_font_size9 = 233
        self.test_font_size10 = 666
        self.test_font_size_x = 2333

        self.test_color1 = (255, 0, 0, 255)
        self.test_color2 = (0, 255, 0, 255)
        self.test_color3 = (0, 0, 255, 255)
        self.test_color4 = (255, 255, 0, 255)
        self.test_color5 = (0, 255, 255, 255)
        self.test_color6 = (255, 0, 255, 255)
        self.test_color7 = (255, 255, 255, 255)
        self.test_color8 = (0, 0, 0, 255)
        self.test_color9 = (123, 123, 123, 255)
        self.test_color10 = (233, 233, 233, 255)
        self.test_color_x = (66, 66, 66, 255)

    def test_specified_letter_generator(self):

        test_image1 = SpecifiedLetterGenerator(self.test_letter_input1, self.font_type, self.test_font_size1, self.test_color1).generate_specified_letter()
        test_image2 = SpecifiedLetterGenerator(self.test_letter_input2, self.font_type, self.test_font_size2, self.test_color2).generate_specified_letter()
        test_image3 = SpecifiedLetterGenerator(self.test_letter_input3, self.font_type, self.test_font_size3, self.test_color3).generate_specified_letter()
        test_image4 = SpecifiedLetterGenerator(self.test_letter_input4, self.font_type, self.test_font_size4, self.test_color4).generate_specified_letter()
        test_image5 = SpecifiedLetterGenerator(self.test_letter_input5, self.font_type, self.test_font_size5, self.test_color5).generate_specified_letter()
        test_image6 = SpecifiedLetterGenerator(self.test_letter_input6, self.font_type, self.test_font_size6, self.test_color6).generate_specified_letter()
        test_image7 = SpecifiedLetterGenerator(self.test_letter_input7, self.font_type, self.test_font_size7, self.test_color7).generate_specified_letter()
        test_image8 = SpecifiedLetterGenerator(self.test_letter_input8, self.font_type, self.test_font_size8, self.test_color8).generate_specified_letter()
        test_image9 = SpecifiedLetterGenerator(self.test_letter_input9, self.font_type, self.test_font_size9, self.test_color9).generate_specified_letter()
        test_image10 = SpecifiedLetterGenerator(self.test_letter_input10, self.font_type, self.test_font_size10, self.test_color10).generate_specified_letter()
        test_image_x = SpecifiedLetterGenerator(self.test_letter_input_x, self.font_type, self.test_font_size_x, self.test_color_x).generate_specified_letter()

        self.assertTrue(abs((test_image1.height) - (self.test_font_size1 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image2.height) - (self.test_font_size2 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image3.height) - (self.test_font_size3 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image4.height) - (self.test_font_size4 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image5.height) - (self.test_font_size5 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image6.height) - (self.test_font_size6 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image7.height) - (self.test_font_size7 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image8.height) - (self.test_font_size8 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image9.height) - (self.test_font_size9 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image10.height) - (self.test_font_size10 * 6832.0 / 10000.0)) < 3)
        self.assertTrue(abs((test_image_x.height) - (self.test_font_size_x * 6832.0 / 10000.0)) < 3)

        self.assertTrue(test_image1.load()[0, 0] == (self.test_color1))
        self.assertTrue(test_image1.load()[test_image1.width-1, test_image1.height-1] == (self.test_color1))
        self.assertTrue(test_image1.load()[test_image1.width/2, test_image1.height/2] == (self.test_color1))

        self.assertTrue(test_image2.load()[0, 0] == (self.test_color2))
        self.assertTrue(test_image2.load()[test_image2.width-1, test_image2.height-1] == (self.test_color2))
        self.assertTrue(test_image2.load()[test_image2.width/2, test_image2.height/2] == (self.test_color2))

        self.assertTrue(test_image3.load()[0, 0] == (self.test_color3))
        self.assertFalse(test_image3.load()[test_image3.width-1, test_image3.height-1] == (self.test_color3))
        self.assertTrue(test_image3.load()[test_image3.width/2, test_image3.height/2] == (self.test_color3))

        self.assertTrue(test_image4.load()[0, 0] == (self.test_color4))
        self.assertTrue(test_image4.load()[test_image4.width-1, test_image4.height-1] == (self.test_color4))
        self.assertTrue(test_image4.load()[test_image4.width/2, test_image4.height/2] == (self.test_color4))

        self.assertTrue(test_image5.load()[0, 0] == (self.test_color5))
        self.assertFalse(test_image5.load()[test_image5.width-1, test_image5.height-1] == (self.test_color5))
        self.assertTrue(test_image5.load()[test_image5.width/2, test_image5.height/2] == (self.test_color5))

        self.assertTrue(test_image6.load()[0, 0] == (self.test_color6))
        self.assertTrue(test_image6.load()[test_image6.width-1, test_image6.height-1] == (self.test_color6))
        self.assertTrue(test_image6.load()[test_image6.width/2, test_image6.height/2] == (self.test_color6))

        self.assertTrue(test_image7.load()[0, 0] == (self.test_color7))
        self.assertTrue(test_image7.load()[test_image7.width-1, test_image7.height-1] == (self.test_color7))
        self.assertTrue(test_image7.load()[test_image7.width/2, test_image7.height/2] == (self.test_color7))

        self.assertTrue(test_image8.load()[0, 0] == (self.test_color8))
        self.assertFalse(test_image8.load()[test_image8.width-1, test_image8.height-1] == (self.test_color8))
        self.assertTrue(test_image8.load()[test_image8.width/2, test_image8.height/2] == (self.test_color8))

        self.assertTrue(test_image9.load()[0, 0] == (self.test_color9))
        self.assertTrue(test_image9.load()[test_image9.width-1, test_image9.height-1] == (self.test_color9))
        self.assertTrue(test_image9.load()[test_image9.width/2, test_image9.height/2] == (self.test_color9))

        self.assertTrue(test_image10.load()[0, 0] == (self.test_color10))
        self.assertFalse(test_image10.load()[test_image10.width-1, test_image10.height-1] == (self.test_color10))
        self.assertTrue(test_image10.load()[test_image10.width/2, test_image10.height/2] == (self.test_color10))

        self.assertTrue(test_image_x.load()[0, 0] == (self.test_color_x))
        self.assertTrue(test_image_x.load()[test_image_x.width-1, test_image_x.height-1] == (self.test_color_x))
        self.assertTrue(test_image_x.load()[test_image_x.width/2, test_image_x.height/2] == (self.test_color_x))

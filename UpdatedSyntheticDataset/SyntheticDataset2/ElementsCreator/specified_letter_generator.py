from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SyntheticDataset2.ImageOperations import *
import random

class SpecifiedLetterGenerator(object):

    def __init__(self, letter_input, font_type, font_size, color):
        """
        Construct the SpecifiedLetterGenerator class
        :param letter_input: the intended letter to create
        :param font_type: the intended font_type of the letter
        :param font_size: the intended font_size of the letter
        :param color: the intended color of the letter
        :type letter_input: string
        :type font_type: a font file
        :type font_size: int
        :type color: (R, G, B, A)
        :type R, G, B, and A: int from 0 to 255
        """
        self.letter_input = letter_input
        self.font_type = font_type
        self.font_size = font_size
        self.letter_color = color
        self.letter_ratio = 10000.0 / 6832.0
        self.background_color = (255, 255, 255, 0)

    def generate_specified_letter(self):
        """
        Generate an image of a specified letter
        1) Generate a transparent background as raw_image
        2) Draw a specified letter onto the raw_image
        3) Mask the raw_image, transforming it into the clean_image
        4) Crop out the letter from the clean_image as the resultant
        5) return the resultant
        """
        image_dimension = self.font_size * self.letter_ratio
        raw_image = Image.new("RGBA", (int(image_dimension), int(image_dimension)), self.background_color)
        draw = ImageDraw.Draw(raw_image)
        font = ImageFont.truetype(self.font_type, self.font_size)
        draw.text((1, 1), self.letter_input, self.letter_color, font = font)
        clean_image = ImageMasker.mask_image(raw_image, raw_image.load(), self.letter_color, self.background_color)
        resultant = BoundedImageCropper.crop_bounded_image(clean_image, clean_image.load(), self.letter_color)
        return resultant

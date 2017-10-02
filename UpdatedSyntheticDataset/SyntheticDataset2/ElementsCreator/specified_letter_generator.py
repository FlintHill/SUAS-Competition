from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SyntheticDataset2.ImageOperations import *
import random

class SpecifiedLetterGenerator(object):

    def __init__(self, letter_input, font_size, color):
        """
        Construct the SpecifiedLetterGenerator class
        :param letter_input: the intended letter to create
        :param font_size: the intended font_size of the letter
        :param color: the intended color of the letter
        :type letter_input: string
        :type font_size: int
        :type color: (R, G, B, A)
        """
        self.letter_ratio = 10000.0 / 6832.0
        self.letter_input = letter_input
        self.font_size = font_size
        self.letter_color = color
        self.background_color = (255, 255, 255, 0)

    def specified_letter_generator(self):
        """
        Generate an image of a specified letter
        1) Generate a transparent background as raw_image
        2) Draw a specified letter onto the raw_image
        3) Mask the raw_image, transforming it into the clean_image
        4) Crop out the letter from the clean_image as the resultant
        5) return the resultant
        """
        image_dimention = self.font_size * self.letter_ratio
        raw_image = Image.new("RGBA", (int(image_dimention), int(image_dimention)), self.background_color)
        draw = ImageDraw.Draw(raw_image)
        font = ImageFont.truetype("UpdatedSyntheticDataset/data/fonts/Blockletter.otf", self.font_size)
        draw.text((1, 1), self.letter_input, self.letter_color, font = font)
        clean_image = ImageMasker.maskImage(raw_image, raw_image.load(), self.letter_color, self.background_color)
        resultant = BoundedImageCropper.cropBoundedImage(clean_image, clean_image.load(), self.letter_color)
        return resultant

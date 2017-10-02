from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SyntheticDataset2.ImageOperations import *
import random

class SpecifiedLetterGenerator(object):

    def __init__(self, letter_input, font_size, color):
        """
        The font to height ratio of block letters.
        """
        self.letter_ratio = 10000.0 / 6832.0
        self.letter_input = letter_input
        self.font_size = font_size
        self.letter_color = color
        self.background_color = (255, 255, 255, 0)

    def specified_letter_generator(self):
        """
        inputs a letter (string), font_size(int), and color(RGBA values), outputs an image.
        """
        image_dimention = self.font_size * self.letter_ratio
        raw_image = Image.new("RGBA", (int(image_dimention), int(image_dimention)), self.background_color)
        draw = ImageDraw.Draw(raw_image)
        font = ImageFont.truetype("UpdatedSyntheticDataset/data/fonts/Blockletter.otf", self.font_size)
        draw.text((1, 1), self.letter_input, self.letter_color, font = font)
        clean_image = ImageMasker.maskImage(raw_image, raw_image.load(), self.letter_color, self.background_color)
        resultant = BoundedImageCropper.cropBoundedImage(clean_image, clean_image.load(), self.letter_color)
        return resultant

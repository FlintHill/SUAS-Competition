from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SyntheticDataset2.ImageOperations import *
import random

class RandomLetterGenerator(object):

    def __init__(self, font_size, color):
        """
        Construct the RandomLetterGenerator class
        :param font_size: the intended font_size of the letter
        :param color: the intended color of the letter
        :type font_size: int
        :type color: (R, G, B, A)
        """
        self.font_size = font_size
        self.letter_color = color
        self.letter_list = ["A", "B", "c", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.letter_ratio = 10000.0 / 6832.0
        self.background_color = (255, 255, 255, 0)

    def random_letter_generator(self):
        """
        Generate an image of a random letter
        1) Generate a transparent background as raw_image
        2) Draw a random letter onto the raw_image
        3) Mask the raw_image, transforming it into the clean_image
        4) Crop out the letter from the clean_image as the resultant
        5) return the resultant
        """
        image_dimention = self.font_size * self.letter_ratio
        raw_image = Image.new("RGBA", (int(image_dimention), int(image_dimention)), self.background_color)
        draw = ImageDraw.Draw(raw_image)
        font = ImageFont.truetype("UpdatedSyntheticDataset/data/fonts/Blockletter.otf", self.font_size)
        draw.text((1, 1), self.letter_list[random.randint(0, 25)], self.letter_color, font = font)
        clean_image = ImageMasker.maskImage(raw_image, raw_image.load(), self.letter_color, self.background_color)
        resultant = BoundedImageCropper.cropBoundedImage(clean_image, clean_image.load(), self.letter_color)
        return resultant

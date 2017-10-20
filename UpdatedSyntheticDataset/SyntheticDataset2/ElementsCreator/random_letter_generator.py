from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random

class RandomLetterGenerator(LetterGenerator):

    def __init__(self, font_type, font_size, color):
        """
        Construct the RandomLetterGenerator class
        :param font_type: the intended font_type of the letter
        :param font_size: the intended font_size of the letter
        :param color: the intended color of the letter
        :type font_type: a font file
        :type font_size: int
        :type color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        """

        super(RandomLetterGenerator, self).__init__(font_type, font_size, color)

        self.letter_list = ["A", "B", "c", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.letter_ratio = 10000.0 / 6832.0
        self.background_color = (255, 255, 255, 0)

    def generate_random_letter(self):
        """
        Generate an image of a random letter
        1) Generate a transparent background as raw_image
        2) Draw a random letter onto the raw_image
        3) Mask the raw_image, transforming it into the clean_image
        4) Crop out the letter from the clean_image as the resultant
        5) return the resultant
        """
        image_dimension = self.font_size * self.letter_ratio
        raw_image = RawImageGenerator.generate_raw_image(int(image_dimension), int(image_dimension), self.background_color)
        draw = ImageDraw.Draw(raw_image)
        font = ImageFont.truetype(self.font_type, self.font_size)
        draw.text((1, 1), self.letter_list[random.randint(0, 25)], self.letter_color, font = font)
        clean_image = ImageMasker.mask_image(raw_image, raw_image.load(), self.letter_color, self.background_color)
        resultant = BoundedImageCropper.crop_bounded_image(clean_image, clean_image.load(), self.letter_color)
        return resultant

from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random

test_specified_letter_generator = SpecifiedLetterGenerator("X", "UpdatedSyntheticDataset/data/fonts/Blockletter.otf", 454, (0, 0, 0, 255))
image1 = test_specified_letter_generator.generate_specified_letter()

"""
image2 = ImageExtender.extend_image(image1, int(image1.width), int(image1.width))
image2.show()

image3 = GaussianNoiseGenerator.generate_gaussian_noise_by_level(image2, 5.5, image1.width)
image3.show()

image4 = BoundedImageCropper.crop_bounded_image_inverse(image3, image3.load(), (255,255,255,0))
image4.show()
"""


image2 = NoisedImageGenerator.generate_noised_image_by_level(image1, 20)
image2.show()

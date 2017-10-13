from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *
from SyntheticDataset2.ImageCreator import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random

"""
test_specified_letter_generator = SpecifiedLetterGenerator("X", "UpdatedSyntheticDataset/data/fonts/Blockletter.otf", int(500*(10000.0 / 6832.0)), (0, 0, 0, 255))
image1 = test_specified_letter_generator.generate_specified_letter()

image2 = ImageExtender.extend_image(image1, int(image1.width), int(image1.width))
image2.show()

image3 = GaussianNoiseGenerator.generate_gaussian_noise_by_level(image2, 5.5, image1.width)
image3.show()

image4 = BoundedImageCropper.crop_bounded_image_inverse(image3, image3.load(), (255,255,255,0))
image4.show()

image2 = NoisedImageGenerator.generate_noised_image_by_level(image1, 20)

image3 = Trapezoid(1500, 3000, 1500, (255, 255, 255, 255), 0).draw()

image4 = ImagePaster.paste_images(image3, image1)
image4.show()
"""
"""
image1 = TargetCreator.create_specified_single_target(21, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image1.show()
image2 = TargetCreator.create_specified_single_target(22, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image2.show()
image3 = TargetCreator.create_specified_single_target(23, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image3.show()
image4 = TargetCreator.create_specified_single_target(24, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image4.show()
image5 = TargetCreator.create_specified_single_target(25, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image5.show()
image6 = TargetCreator.create_specified_single_target(26, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image6.show()
image7 = TargetCreator.create_specified_single_target(27, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image7.show()
image8 = TargetCreator.create_specified_single_target(28, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image8.show()
image9 = TargetCreator.create_specified_single_target(29, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image0.show()
image10 = TargetCreator.create_specified_single_target(30, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image10.show()
"""
image11 = TargetCreator.create_specified_single_target(31, "X", 500, 2, (255, 255, 255, 255), (0, 0, 0, 255))
image11.show()

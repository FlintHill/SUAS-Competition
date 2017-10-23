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
"""
"""
image4 = BoundedImageCropper.crop_bounded_image_inverse(image3, image3.load(), (255,255,255,0))
image4.show()

image2 = NoisedImageGenerator.generate_noised_image_by_level(image1, 20)

image3 = Trapezoid(1500, 3000, 1500, (255, 255, 255, 255), 0).draw()

image4 = ImagePaster.paste_images(image3, image1)
image4.show()
"""
"""
i = 0
while i < 10:
    image5 = RandomTargetCreator.create_random_target([500, 1000], [2.0, 3.0])
    image5.show()
    i = i + 1
"""
"""
image6 = TargetWithBackgroundCreator.create_random_target_with_background([500, 1000], [2.0, 3.0], "UpdatedSyntheticDataset/backgrounds")
image6.show()
"""
"""
i = 0
while i < 10:
    image6 = TargetWithBackgroundCreator.create_random_target_with_specified_background([500, 1000], [2.0, 3.0], "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG")
    image6.show()
    i = i + 1
j = 0
while j < 10:
    image7 = NoisedTargetWithBackgroundCreator.create_random_noised_target_with_specified_background([500, 1000], [2.0, 3.0], "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 2)
    image7.show()
    j = j + 1
k = 0
while k < 10:
    image8 = NoisedTargetWithNoisedBackgroundCreator.create_random_noised_target_with_specified_noised_background([50, 100], [1.5, 2.5], "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 2)
    image8.show()
    k = k + 1
"""

image1 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("circle", "N", "A", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 87.4)
image1.show()
"""
image2 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("half_circle", "N", "B", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image3 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("quarter_circle", "N", "C", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image4 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("triangle", "N", "D", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image5 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("cross", "N", "E", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image6 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("star", "N", "F", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image7 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("rectangle", "NS", "G", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image8 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("square", "N", "H", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image9 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("pentagon", "N", "I", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image10 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("hexagon", "N", "J", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image11 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("heptagon", "N", "K", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image12 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("octagon", "N", "L", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image13 = TargetWithBackgroundCreator.create_specified_target_with_specified_background("trapezoid", "N", "M", 1000, 1.5, (255, 255, 255, 255), (0, 0, 0, 255), "UpdatedSyntheticDataset/backgrounds/competition_grass_1.JPG", 0)

image1.show()
image2.show()
image3.show()
image4.show()
image5.show()
image6.show()
image7.show()
image8.show()
image9.show()
image10.show()
image11.show()
image12.show()
image13.show()
"""

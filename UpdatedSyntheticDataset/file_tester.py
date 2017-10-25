from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *
from SyntheticDataset2.ImageCreator import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random

#image1 = TargetMapCreator.create_random_target_map(20, [50, 100], [1.5, 2.5], "/Users/zyin/Desktop/competition_grass_1.JPG")
#image1.show()

#image1 = TargetMapCreator.create_random_target_map(10, [50, 100], [1.5, 2.5], "tests/images/competition_grass_1.JPG")
#image1.show()
"""
image1 = SpecifiedTargetCreator.create_specified_target("circle", "N", "Z", 500, 2, (255, 255, 255, 255), (255, 0, 0, 255), 45)
ImageResizer.resize_image_free(image1, 30.0).show()

image2 = SpecifiedTargetCreator.create_specified_target("circle", "N", "Z", 1000, 2, (255, 255, 255, 255), (255, 0, 0, 255), 45)
ImageResizer.resize_image_free(image2, 30.0).show()
"""
image3 = TargetWithBackgroundCreator.create_random_target_with_specified_background([500, 1000], [1.5, 2.5], "/Users/zyin/Desktop/competition_grass_1.JPG", -1, 0)
image3.show()

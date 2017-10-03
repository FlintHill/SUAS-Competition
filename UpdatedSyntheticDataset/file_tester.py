from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random

test_random_letter_generator = RandomLetterGenerator("UpdatedSyntheticDataset/data/fonts/Blockletter.otf", 454, (0, 0, 0, 255))
test_random_letter_generator.generate_random_letter().show()

test_specified_letter_generator = SpecifiedLetterGenerator("Z", "UpdatedSyntheticDataset/data/fonts/Blockletter.otf", 565, (0, 0, 0, 255))
test_specified_letter_generator.generate_specified_letter().show()

"""
image_dimension = 1000 * 2
image = Image.new("RGBA", (image_dimension, image_dimension), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("UpdatedSyntheticDataset/data/fonts/Blockletter.otf", 1000)
draw.text((0, 0), "Z", (0, 0, 0, 255), font = font)
image.show()

dimension = image.size
pixel_data = image.load()
list_of_x = []
list_of_y = []

for x in range(0, dimension[0]):
    for y in range(0, dimension[1]):
        if  pixel_data[x,y] == (0, 0, 0, 255):
            list_of_x.append(x)
            list_of_y.append(y)

left_x = min(list_of_x)-1
right_x = max(list_of_x)+2
up_y = min(list_of_y)-1
low_y = max(list_of_y)+2
image.crop((left_x, up_y, right_x, low_y)).show()
"""

import numpy
from PIL import Image
import argparse
import cv2
import os
import timeit
from UpdatedImageProcessing import *

<<<<<<< HEAD
image_path = (os.path.expanduser("~/Desktop/2.jpg"))
print SingleTargetMapDetector.detect_single_target_map(image_path)

||||||| merged common ancestors
image = Image.open("/Users/zyin/Desktop/Image_Processing_Report/Images/9.jpg - 1.png")

image_2 = ColorOperations.apply_color_quantization(image, 3)
#image_2 = BackgroundColorNullifier.nullify_color_and_recrop_target(image, 5)
image_2.show()

=======
image_path = (os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps/2.jpg"))
print SingleTargetMapDetector.detect_single_target_map(image_path)
'''
image = Image.open("/Users/zyin/Desktop/Image_Processing_Report/Images/9.jpg - 1.png")

image_2 = ColorOperations.apply_color_quantization(image, 3)
#image_2 = BackgroundColorNullifier.nullify_color_and_recrop_target(image, 5)
image_2.show()
'''
>>>>>>> For rebase
#Run IntegratedImageProcessing
"""
target_map_path = os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps")
autonomous_image_processing_save_path = os.path.expanduser("~/Desktop/Save_Path")

_processing(target_map_path, autonomous_image_processing_save_path)
"""

#Find average color of an image
'''
target_map_image = Image.open("/Users/zyin/Desktop/Synthetic_Dataset/Backgrounds/06150460.jpg")

total_r = 0
total_g = 0
total_b = 0
area = 0
pixel_access_target_map_image = target_map_image.load()

for x in range(target_map_image.width):
    for y in range(target_map_image.height):
        area += 1
        total_r += pixel_access_target_map_image[x, y][0]
        total_g += pixel_access_target_map_image[x, y][1]
        total_b += pixel_access_target_map_image[x, y][2]

average_r = total_r / area
average_g = total_g / area
average_b = total_b / area
average_color = (average_r, average_g, average_b)

print average_color
print ColorOperations.find_percentage_difference((38, 37, 19), average_color)
'''

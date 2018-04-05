from UpdatedImageProcessing import *
from PIL import Image
import cv2
import numpy
import os
from bounding_box import BoundingBox
from convex_corners import convex_corners, convex_corners_cross


testpath = "../../../../../targets_full_dataset/cross/6.png"
dataset = "../../../../../targets_full_dataset/cross"

"""
for filename in os.listdir(dataset):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img = Image.open(os.path.join(dataset, filename))
        print(convex_corners(img))
"""



test_img = Image.open(testpath)

print(convex_corners_cross(test_img, show_plot=True))


"""
test_img = Image.open(testpath)

b = BoundingBox(test_img, show_plot=False)
print(b.get_area_difference())
"""

"""
for filename in os.listdir(dataset):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img = Image.open(os.path.join(dataset, filename))
        b = BoundingBox(img)
        c = b.get_area_difference()
        if(c < 100):
            print(c)
            print(filename)
            b.show_plot()
"""

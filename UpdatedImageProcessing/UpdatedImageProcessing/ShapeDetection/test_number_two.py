from UpdatedImageProcessing.ShapeDetection import utils
from PIL import Image
import cv2
import numpy
import os
from shape_classification_two import ShapeClassificationTwo
from settings import ShapeDetectionSettings


testpath = "../../../../targets_full_dataset/cross/17.png"
dataset = "../../../../targets_full_dataset/star"

otherpath = "target_detection_masks/circle/circle1-1.png"

manual = os.path.expanduser("~/Desktop/Image_Processing_Report/Images")

"""
shape_mask_img = Image.open(testpath)
shape_mask_img = utils.generate_gaussian_noise_by_level(shape_mask_img, 5, shape_mask_img.width)
cv2.imshow('image',utils.alpha_fill(shape_mask_img))
cv2.waitKey(0)
cv2.destroyAllWindows()

_,contours,_ = cv2.findContours(shape_mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
shape_contour = contours[0]
"""


for filename in os.listdir(manual):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        shape = ShapeClassificationTwo(os.path.join(manual, filename)).get_shape_type()
        #psc = utils.PolarSideCounter(utils.alpha_trace(Image.open(os.path.join(dataset, filename))))

        print(filename)
        print(shape)



"""
target_mask_img = utils.alpha_fill(Image.open(testpath))
_,contours,_ = cv2.findContours(target_mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
target_contour = contours[0]

shape_mask_img = cv2.imread(otherpath,0)
_,contours,_ = cv2.findContours(shape_mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
shape_contour = contours[0]

print(cv2.matchShapes(shape_contour, target_contour, 1, 0.0))
"""

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

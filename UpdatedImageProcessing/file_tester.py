from ImageProcessing2.TargetDetection import *
from PIL import Image
import cv2
import numpy

single_target_crop = Image.open("/Users/zyin/Desktop/Synthetic_Dataset/Answers/modular_single_targets_with_background/1.png")

print single_target_crop.load()[0, 0]
#ConnectedComponentLabeler.label_connected_components(single_target_crop)

'''
target_image = numpy.array(single_target_crop)
target_image = cv2.cvtColor(target_image, cv2.COLOR_RGB2GRAY)

#img = cv2.imread("/Users/zyin/Desktop/Synthetic_Dataset/Answers/modular_single_targets_with_background/1.png")
img = cv2.threshold(target_image, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
ret, labels = cv2.connectedComponents(img)

# Map component labels to hue val
label_hue = numpy.uint8(179 * labels/numpy.max(labels))


blank_ch = 255*numpy.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

# cvt to BGR for display
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

# set bg label to black
labeled_img[label_hue==0] = 0

image = Image.fromarray(labeled_img, 'RGB')
image.show()
'''

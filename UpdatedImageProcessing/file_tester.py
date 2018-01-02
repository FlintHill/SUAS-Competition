import numpy
import cv2
import io
from matplotlib import pyplot
import io
from PIL import Image
from ImageProcessing2.TargetDetection import *

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(TargetDetectionSettings.TARGET_MAPS_PATH + "/2.jpg", 0)

blurred = cv2.GaussianBlur(image, (3, 3), 0)

edge = cv2.Canny(blurred, 100, 200)

#image = Image.fromarray(wide, 'RGB')
#image.show()

_, contours, _= cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


cnt = contours[1]
M = cv2.moments(cnt)

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

print cx

'''
cv2.imshow("Original", image)
cv2.imshow("Edges", edge)
cv2.waitKey(0)
'''





'''
print image_with_keypoints
image = Image.fromarray(image_with_keypoints, 'RGB')
print image
#image.show()
'''
'''
# show the images
image = Image.fromarray(wide, 'RGBA')
image.show()

# show the images
cv2.imshow("Original", image)
cv2.imshow("Edges", numpy.hstack([wide, tight]))
cv2.waitKey(0)
'''

from UpdatedImageProcessing import *
from PIL import Image
import os
import cv2
import numpy

testpath = "../../../../test_targets/22.png"
noise = "../../../../test_targets/noise_targets/1-1.png"
DATASET_PATH = "/Users/jmoxley/Desktop/compsci/SUAS/test_targets/squares"
full_dataset = "../../../../targets_full_dataset/circle"



#test 1
sc = ShapeClassification(testpath)
#canny_img = alpha_trace(testpath)
#print(PolarSideCounter(canny_img, show_plot=True).get_circle_score())
print(sc.get_shape_type())


"""
#test 2
canny_img = alpha_trace(testpath)
canny_img.show()
psc = PolarSideCounter(canny_img, show_plot=True)
print(psc.get_circle_score())
"""

"""
#test 3
for filename in os.listdir(DATASET_PATH):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        sc = ShapeClassification(os.path.join(DATASET_PATH, filename))
        #sc = PolarSideCounter(alpha_trace(os.path.join(DATASET_PATH, filename)))
        print(sc.get_shape_type())
"""

"""
# test 4
img = cv2.imread(testpath)
canny_img = numpy.array(alpha_trace(testpath))

rho = 1
theta = 1*numpy.pi/180
threshold = 20

lines = cv2.HoughLines(canny_img, rho, theta, threshold)
sides = []
if type(lines) != "NoneType":
    print len(lines)
    for i in range(len(lines)):
        hl = HoughLine(lines[i])

        if len(sides) == 0:
            sides.append(hl)
            points = hl.get_plot_points()
            cv2.line(img,points[0],points[1],(0,255,),2)
        else:
            unique_line = True
            for i in range(len(sides)):
                if abs(sides[i].get_theta() - hl.get_theta()) < 0.5:
                    if abs(sides[i].get_rho() - hl.get_rho()) < 50:
                        unique_line = False
                        break
            if unique_line:
                sides.append(hl)
                points = hl.get_plot_points()
                cv2.line(img,points[0],points[1],(0,255,),2)

print(len(sides))
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

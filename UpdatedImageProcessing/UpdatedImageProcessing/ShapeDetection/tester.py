from shape_classification import ShapeClassification
from utils import PolarSideCounter
from utils import alpha_trace
from PIL import Image
import os

testpath = "../../../../test_targets/1.png"
DATASET_PATH = "/Users/jmoxley/Desktop/compsci/SUAS/test_targets/squares"


"""
#test 1
sc = ShapeClassification(testpath)
canny_img = alpha_trace(testpath)
#print(PolarSideCounter(canny_img, show_plot=True).get_circle_score())
print(sc.get_shape_type())
"""

"""
#test 2
canny_img = alpha_trace(testpath)
canny_img.show()
psc = PolarSideCounter(canny_img, show_plot=True)
print(psc.get_circle_score())
"""


#test 3
for filename in os.listdir(DATASET_PATH):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        sc = ShapeClassification(os.path.join(DATASET_PATH, filename))
        print(sc.get_shape_type())

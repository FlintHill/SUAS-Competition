from shape_classification import ShapeClassification
from utils import PolarSideCounter
from utils import alpha_trace
from PIL import Image

testpath = "../../../../test_targets/47.png"

"""
#test 1

sc = ShapeClassification(testpath)

print(sc.get_shape_type())
"""


#test 2
canny_img = alpha_trace(testpath)
canny_img.show()
psc = PolarSideCounter(canny_img, show_plot=True)
print(psc.get_circle_score())

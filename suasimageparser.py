from SUASImageParser import ImageParser

from options import parseOptions
from options import getOption

import cv2


# ------------------------ Creating option parser -------------------------
parseOptions()


# ------------------------ Loading image & parsing ------------------------
my_parser = ImageParser(mode="ADLC", debug=True)

img = my_parser.parse(getOption("image"))


# ------------------------ Displaying loaded image ------------------------
cv2.imshow("Parsed", img)
cv2.waitKey( 0 )
cv2.destroyAllWindows()

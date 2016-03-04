from SUASImageParser import ImageParser

import cv2


# ------------------------ Loading image & parsing ------------------------
my_parser = ImageParser("ADLC", True)
img = my_parser.parse('images/IMG_0160.JPG')


# ------------------------ Displaying loaded image ------------------------
cv2.imshow("Parsed", img)
cv2.waitKey( 0 )
cv2.destroyAllWindows()

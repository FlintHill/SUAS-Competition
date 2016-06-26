from SUASImageParser import ImageParser
from SUASImageParser.utils.color import bcolors

from options import parseOptions
from options import getOption

import cv2


# ------------------------ Creating option parser -------------------------
parseOptions()


# ------------------------ Ensuring image provided ------------------------
if getOption("image") == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide an image to parse")
    exit(0)


# ------------------------ Loading image & parsing ------------------------
my_parser = ImageParser(mode="ADLC", debug=True)

img = my_parser.parse(getOption("image"))


# ------------------------ Displaying loaded image ------------------------
cv2.imshow("Parsed", img)
cv2.waitKey( 0 )
cv2.destroyAllWindows()

from SUASImageParser.utils.image import Image
from SUASImageParser.utils.color import bcolors

import cv2
import timeit

class ADLCParser:
    """
    General class for processing ADLC-related images
    """

    def __init__(self, **kwargs):
        self.image = Image()
        self.debug = False
        self.start_time = None

        self.PIXEL_COLOR_THRESHOLD = 0
        self.BLACK_COLOR_THRESHOLD = 5
        self.LOWER_CONTOUR_AREA = 1200
        self.HIGHER_CONTOUR_AREA = 100000
        self.ADJACENT_OBJECT_INDEX = 0

    def set_debug(self, updated_debug):
        """
        Sets the debug variable to the value of "debug" which determines
        whether status updates should be printed to terminal throughout
        the parsing process.
        """
        self.debug = updated_debug

    def simple_parse(self, image):
        """
        Returns true/false whether an in-depth parse should be applied. This
        method only does a couple of quick checks to remove images where it is
        clear there are no targets.
        """
        # @TODO: Implement simple parsing

        return True

    def parse(self, filename):
        """
        Parses the given image to identify potential ADLC targets. Returns a
        list of possible targets.
        """
        # If debugging is enabled, setting the time started
        if self.debug:
            self.start_time = timeit.default_timer()

        # Load image
        self.image.load(filename)

        # Convert image to HSV then to GRAY to help make it easy to identify
        #   possible targets
        if self.debug:
            print bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Converting image to HSV"
        hsv = cv2.cvtColor(self.image.get_image(), cv2.COLOR_BGR2HSV)

        if self.debug:
            print bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Converting HSV to GRAY"
        img = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)


        # Thresholding & getting contours
        #ret,thresh = cv2.threshold(img,127,255,0)
        #ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
        thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,14)
        _,contours,hierarchy = cv2.findContours(thresh, 1, 2)

        cv2.drawContours(img, contours, -1, (255,0,0), 3)

        # If debugging is enabled, calculating time took to parse
        if self.debug:
            end_time = timeit.default_timer()
            print bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Took " + str(end_time - self.start_time) + " SECONDS to parse the image"

        # Returning the grayed out image
        return img

    def identify_characteristics(self, target):
        """
        Identifies the characteristics of the target "target" and returns
        them as a dictionary object
        """
        # @TODO: Implement characteristic identification

        return {}

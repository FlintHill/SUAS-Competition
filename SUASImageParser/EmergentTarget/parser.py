from SUASImageParser.utils.image import Image
from SUASImageParser.utils.color import bcolors

import cv2

class EmergentTargetParser:
    """
    General class for processing EmergentTarget-related images
    """

    def __init__(self):
        self.image = Image()
        self.debug = False

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
        Parses the given image to identify potential EmergentTarget targets.
        Returns a list of possible targets.
        """
        # Load image
        self.image.load(filename)

        # Convert image to HSV then to GRAY to help make it easy to identify
        #   possible targets
        if self.debug:
            print bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Converting image to HSV"
        hsv = cv2.cvtColor(self.image.get_image(), cv2.COLOR_BGR2HSV)

        if self.debug:
            print bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Converting HSV to GRAY"
        grayed = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)

        # Returning the grayed out image
        return grayed

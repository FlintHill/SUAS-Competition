from SUASImageParser.utils.image import Image
from SUASImageParser.utils.color import bcolors
from SUASImageParser.modules import k_means
from SUASImageParser.modules import summing

import cv2
import timeit
import numpy as np


class ADLCParser:
    """
    General class for processing ADLC-related images
    """

    def __init__(self, **kwargs):
        self.image = Image()
        self.debug = kwargs.get("debug")

        self.LOWER_CONTOUR_AREA = 1200
        self.HIGHER_CONTOUR_AREA = 100000

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
            print(bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Converting image to HSV")
        hsv = cv2.cvtColor(self.image.get_image(), cv2.COLOR_BGR2HSV)

        if self.debug:
            print(bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Converting HSV to GRAY")
        img = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)

        # Identifying targets
        if self.debug:
            print(bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Identifying targets")
        targets = self.identify_targets(img)

        # Identifying target characteristics
        if self.debug:
            print(bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Identifying target characteristics")
        target_characteristics = self.identify_characteristics(targets)

        # If debugging is enabled, calculating time took to parse
        if self.debug:
            end_time = timeit.default_timer()
            print(bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Took " + str(end_time - self.start_time) + " SECONDS to parse the image")

        # Returning the grayed out image
        return targets, target_characteristics

    def identify_targets(self, img):
        """
        Identifies possible targets and returns the list of those targets (in
        the form of cropped images)
        """
        # Creating holder variables
        targets = []

        # Thresholding image
        # @TODO: Figure out a way to optimize this process to pick the correct
        #   thresholding method & settings
        #ret,thresh = cv2.threshold(img,127,255,0)
        #ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
        thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,14)

        # Getting contours
        # @TODO: Investigate possibly using a different method to avoid this.
        #   Line detection might be a much better route to go (if used in
        #   conjunction with approxPolyDP() & edge vectorization to identify
        #   shapes)
        _,contours,hierarchy = cv2.findContours(thresh, 1, 2)

        # Looking for possible targets
        for cnt in contours:
            object_coordinates = np.array(cnt, dtype=np.int32)

            if not (cv2.contourArea(cnt) < self.LOWER_CONTOUR_AREA or cv2.contourArea(cnt) > self.HIGHER_CONTOUR_AREA):
                is_a_target, possible_target = self.parse_possible_target(img, cnt)

                if is_a_target:
                    targets.append(possible_target)

        # @TODO: REMOVE WHEN NOT NEEDED
        cv2.drawContours(img, contours, -1, (255,0,0), 3)

        # Return the identified targets
        # @TODO: return the identified targets and not the given image
        return img

    def parse_possible_target(self, img, contours):
        """
        Parse the possible target and determine whether or not the image
        should be classified as a target.
        """
        # @TODO: Implement target parsing here

        return False, img

    def crop_img(self, contours):
        """
        Cropping self.image based on the passed contour(s)
        """
        # Creating bounding rect & grabbing corresponding part of image
        x,y,w,h = cv2.boundingRect(contours)
        cropped_img = self.image.get_ROI([x, y], [x+w, y+h])

        # Returning cropped image
        return cropped_img

    def identify_characteristics(self, target):
        """
        Identifies the characteristics of the target "target" and returns
        them as a dictionary object
        """
        # @TODO: Implement characteristic identification

        # My thoughts so far to accomplish this is to break the problem down
        #   into the following tasks:
        #   1) Segmentation
        #   2) OCR
        #   3) Pixhawk log parse to gather data about
        #       3a) GPS
        #       3b) Heading
        # I'm not really sure how to implement this process, which is why I am
        #   leaving it in this comment as a "stub" which needs to be resolved.

        # Returning the characteristics for each target
        return {}

from SUASImageParser.utils.image import Image
from SUASImageParser.utils.color import bcolors
from SUASImageParser.modules import k_means
from SUASImageParser.modules import summing
from SUASImageParser.modules import gaussian_blurring

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
        
        # @TODO: Calculate correct lower and upper areas
        self.LOWER_CONTOUR_AREA = kwargs.get("LOWER_CONTOUR_AREA", 1000)
        self.HIGHER_CONTOUR_AREA = kwargs.get("HIGHER_CONTOUR_AREA", 50000)

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
        target_characteristics = None
        if len(targets) > 0:
            print(len(targets))
            for target in targets:
                target_characteristics = self.identify_characteristics(target)
    
                cv2.imshow("target", target)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        # If debugging is enabled, calculating time took to parse
        if self.debug:
            end_time = timeit.default_timer()
            print(bcolors.INFO + "[ Info ]" + bcolors.ENDC + " Took " + str(end_time - self.start_time) + " SECONDS to parse the image")

        # Returning the grayed out image
        return img, target_characteristics

    def identify_targets(self, img):
        """
        Identifies possible targets and returns the list of those targets (in
        the form of cropped images)
        """
        # Creating temp variables
        targets = []

        # Thresholding image
        # @TODO: Figure out a way to optimize this process to pick the correct
        #   thresholding method & settings
        ret,thresh = cv2.threshold(img,127,255,0)
        #ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
        #thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,14)

        # Getting contours
        # @TODO: Investigate possibly using a different method to avoid this.
        #   Line detection might be a much better route to go (if used in
        #   conjunction with approxPolyDP() & edge vectorization to identify
        #   shapes)
        _,contours,hierarchy = cv2.findContours(thresh, 1, 2)

        # Looking for possible targets
        for cnt in contours:
            object_coordinates = np.array(cnt, dtype=np.int32)
    
            if cv2.contourArea(cnt) > self.LOWER_CONTOUR_AREA and cv2.contourArea(cnt) < self.HIGHER_CONTOUR_AREA:
                cv2.drawContours(img, cnt, -1, (255,0,0), 3)
                
                is_a_target, possible_target = self.parse_possible_target(img, cnt)
                if is_a_target:
                    targets.append(possible_target)

        # Return the identified targets
        return targets

    def parse_possible_target(self, img, contours):
        """
        Parse the possible target and determine whether or not the image
        should be classified as a target.
        """
        # Getting target
        cropped_img = k_means.simplify_by_k_means(self.crop_img(contours))
        is_target = True
        
        # Running tests
        is_target = self.color_comparisons(cropped_img)
        
        # Cleaning up the image
        if is_target:
            # Blurring
            cropped_img = gaussian_blurring.gaussian_blurring(cropped_img, 1)
        
        # Getting shape of target to remove false positives
        approx_sides = cv2.approxPolyDP(contours, 0.15 * cv2.arcLength(contours, True), True)
        if len(approx_sides) != 5 and len(approx_sides) != 4 and len(approx_sides) != 3:
            is_target = False

        # Returning results from tests
        return is_target, cropped_img

    def crop_img(self, contours):
        """
        Cropping self.image based on the passed contour(s)
        """
        # Creating bounding rect & grabbing corresponding part of image
        x,y,w,h = cv2.boundingRect(contours)
        cropped_img = self.image.get_ROI([x, y], [x+w, y+h])
        
        # Moving the contours from the main image to this image (editing coordinates to fit the smaller image)
        corrected = contours
        for index in range(len(contours)):
            corrected[index][0][0] = corrected[index][0][0] - x
            corrected[index][0][1] = corrected[index][0][1] - y

        # Creating a mask & drawing the passed contours onto that mask
        mask_img = np.zeros(cropped_img.get_image().shape, dtype=np.uint8)
        
        roi_corners = np.array(corrected, dtype=np.int32)
        black = (255, 255, 255)
        cv2.drawContours(mask_img, [corrected], 0, black, -1)
        
        # Copying over the image inside of the contours
        masked_img = cv2.bitwise_and(cropped_img.get_image(), mask_img)
        
        # Returning the cropped image
        return masked_img

    def color_comparisons(self, img, COLOR_THRESHOLD=5):
        """
        Compare colors in img to ensure that they are sufficietly
        different (removing multiple shades of the same color.
        """
        passes = True
        
        # Finding the colors in the image
        colors = [[255, 255, 255]]
        for x in xrange(0, img.shape[0], 1):
            for y in xrange(0, img.shape[1], 1):
                should_add = True
                for color in colors:
                    if img[x, y, 0] == color[0] and img[x, y, 1] == color[1] and img[x, y, 2] == color[2]:
                        should_add = False
                if should_add:
                    colors.append([img[x, y, 0], img[x, y, 1], img[x, y, 2]])
    
        # Remove useless colors that are in all images
        colors = colors[2:]
        
        # Comparing colors to see if they are multiple shades of the same color
        threshold_num = 0
        for rgb_index in range(3):
            if abs(colors[0][rgb_index] - colors[1][rgb_index]) < COLOR_THRESHOLD:
                threshold_num += 1
        if threshold_num >= 1:
            passes = False
    
        # Return whether the result of the test
        return passes

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

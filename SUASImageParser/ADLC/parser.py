from SUASImageParser.utils.image import Image
from SUASImageParser.utils.color import bcolors
from SUASImageParser.modules import k_means
from SUASImageParser.modules import gaussian_blurring
from SUASImageParser.modules import histogram_equalization
from .characteristic_identifier import CharacteristicIdentifier
import cv2
import timeit
import numpy as np


class ADLCParser:
    """
    General class for processing ADLC-related images
    """

    def __init__(self, **kwargs):
        # Initializing settings
        self.setup(kwargs)

        # Creating instance variables
        self.image = Image()
        self.target_characteristic_identifier = CharacteristicIdentifier()

    def setup(self, settings):
        """
        Initialize all settings
        """
        self.settings = settings

        # Setting up general settings
        self.DEBUG = settings.get("debug", False)

        # Setting up all parsing specific settings
        # @TODO: Calculate correct lower and bounds for target detection
        self.LOWER_CONTOUR_AREA = settings.get("LOWER_CONTOUR_AREA", 500)
        self.HIGHER_CONTOUR_AREA = settings.get("HIGHER_CONTOUR_AREA", 10000)

        self.THRESH_TYPE = cv2.THRESH_BINARY
        self.THRESH_VALUE = settings.get("THRESH_VALUE", 127)
        self.THRESH_POS_VAL = settings.get("THRESH_POS_VAL", 255)

        self.SCALE_FACTOR = settings.get("SCALE_FACTOR", 0.15)

    def set_debug(self, updated_debug):
        """
        Sets the debug variable to the value of "debug" which determines
        whether status updates should be printed to terminal throughout
        the parsing process.
        """
        self.DEBUG = updated_debug

    def parse_file(self, filename):
        """
        Parses the given image to identify potential ADLC targets. Returns a
        list of possible targets.
        """
        self.image.load(filename)

        return self.parse(self.image.get_image())

    def parse(self, img):
        """
        Parses the given image to identify potential ADLC targets. Returns a
        list of possible targets.
        """
        # If debugging is enabled, setting the time started
        if self.DEBUG:
            self.start_time = timeit.default_timer()

        # Load image
        self.image.set_image(img)

        # Convert image to HSV then to GRAY to help make it easy to identify
        #   possible targets
        if self.DEBUG:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Converting image to HSV")
        hsv = cv2.cvtColor(self.image.get_image(), cv2.COLOR_BGR2HSV)

        if self.DEBUG:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Applying histogram equalization")
        equalized = histogram_equalization.histeq(hsv)[0].astype(np.uint8)

        if self.DEBUG:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Converting histogram equalized to GRAY")
        img = cv2.cvtColor(cv2.cvtColor(equalized, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)

        """
        # Test for using OpenCV's Blob detection to identify targets

        detector = cv2.MSER_create(1, 3000, 30000)
        keypoints = detector.detect(equalized)
        keypoints2 = detector.detect((255-img))

        im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, keypoints2, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow("Histogram Equalized with Blobs", im_with_keypoints)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(0)
        """

        if self.DEBUG:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Inverting the image")
        img = (255-img)

        # Identifying targets
        if self.DEBUG:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Identifying targets")
        targets = self.identify_targets(img)

        # Identifying target characteristics
        if self.DEBUG:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Identifying target characteristics")
        target_characteristics = None
        if len(targets) > 0:
            print(len(targets))
            for target in targets:
                target_characteristics = self.identify_characteristics(target)

                #cv2.imshow("target", target)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

        # If debugging is enabled, calculating time took to parse
        if self.DEBUG:
            end_time = timeit.default_timer()
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Took " + str(end_time - self.start_time) + " seconds to parse the image")

        # Returning the grayed out image
        return targets, target_characteristics

    def identify_targets(self, img):
        """
        Identifies possible targets and returns the list of those targets (in
        the form of cropped images)
        """
        # Creating temp variables
        targets = []

        # Thresholding image
        if self.DEBUG:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Thresholding the image")
        # @TODO: Figure out a way to optimize this process to pick the correct
        #   thresholding method & settings
        ret,thresh = cv2.threshold(img, self.THRESH_VALUE, self.THRESH_POS_VAL, self.THRESH_TYPE)
        #thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,14)
        #thresh = cv2.Canny(img,175,225)

        # Getting contours
        if self.DEBUG:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Getting the contours of objects")
        # @TODO: Investigate possibly using a different method to avoid this.
        #   Line detection might be a much better route to go (if used in
        #   conjunction with approxPolyDP() & edge vectorization to identify
        #   shapes)
        _,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 2)

        # Looking for possible targets
        for cnt in contours:
            object_coordinates = np.array(cnt, dtype=np.int32)

            if cv2.contourArea(cnt) > self.LOWER_CONTOUR_AREA and cv2.contourArea(cnt) < self.HIGHER_CONTOUR_AREA:
                cv2.drawContours(img, cnt, -1, (255,0,0), 3)

                is_a_target, possible_target = self.parse_possible_target(img, cnt)
                if is_a_target:
                    if self.DEBUG:
                        print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Found a target")
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
        if not self.is_shape(cropped_img, contours):
            is_target = False

        # Returning results from tests
        return is_target, cropped_img

    def is_shape(self, cropped_img, contours):
        """
        Return true if the cropped image sent to this method is a shape, and
        false if it is not.
        """
        approx_sides = cv2.approxPolyDP(contours, self.SCALE_FACTOR * cv2.arcLength(contours, True), True)
        while (len(approx_sides) != 3 and self.SCALE_FACTOR < 1.0):
            approx_sides = cv2.approxPolyDP(contours, self.SCALE_FACTOR * cv2.arcLength(contours, True), True)

            self.SCALE_FACTOR += 0.01

        return len(approx_sides) == 3

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
        for x in range(0, img.shape[0]):
            for y in range(0, img.shape[1]):
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
            try:
                if abs(colors[0][rgb_index] - colors[1][rgb_index]) < COLOR_THRESHOLD:
                    threshold_num += 1
            except:
                print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Color comparisons threw an exception")
        if threshold_num >= 1:
            passes = False

        # Return whether the result of the test
        return passes

    def identify_characteristics(self, target):
        """
        Identifies the characteristics of the target "target" and returns
        them as a dictionary object
        """
        return self.target_characteristic_identifier.identify_characteristics(target)

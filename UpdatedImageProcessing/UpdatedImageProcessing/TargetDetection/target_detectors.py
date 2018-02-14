import cv2
import numpy
import io
import PIL.ImageOps
from matplotlib import pyplot
from PIL import Image
from .settings import Settings

class TargetDetectors(object):

    """
    The following code is adapted from OpenCV:
    """
    def __init__(self, pil_target_map_image):
        """
        :param pil_target_map_image: the image of the target map

        :type pil_target_map_image: a pil image
        """
        self.pil_target_map_image = pil_target_map_image.convert("RGB")
        self.posterized_pil_target_map_image = PIL.ImageOps.posterize(self.pil_target_map_image, 2)
        self.inverted_pil_target_map_image = PIL.ImageOps.invert(self.posterized_pil_target_map_image)
        self.cv2_target_map_image = cv2.cvtColor(numpy.array(self.inverted_pil_target_map_image), cv2.COLOR_RGB2BGR)

    def detect_blobs(self):
        """
        The algorithm of SimpleBlobDetector follows the following steps:

        Thresholding: Convert the source images to several binary images by
                      thresholding the source image with thresholds starting at
                      minThreshold. These thresholds are incremented by
                      thresholdStep until maxThreshold. So the first threshold
                      is minThreshold, the second is
                      minThreshold + thresholdStep, the third is
                      minThreshold + 2 x thresholdStep, and so on.

        Grouping: In each binary image, connected white pixels are grouped
                  together. Let us call these binary blobs.

        Merging: The centers of the binary blobs in the binary images are
                 computed, and blobs located closer than minDistBetweenBlobs are
                 merged.

        Center & Radius Calculation: The centers and radii of the new merged
                                     blobs are computed and returned.
        """
        #Set up the detector with default parameters.
        params = cv2.SimpleBlobDetector_Params()

        #Set up Thresholds. Values are changed in Settings.
        params.minThreshold = Settings.BLOB_DETECTOR_MINIMUM_THRESHOLD
        params.maxThreshold = Settings.BLOB_DETECTOR_MAXIMUM_THRESHOLD

        #Set up filters. Values are changed in Settings.
        params.filterByArea = Settings.FILTER_BY_AREA_ON
        params.minArea = (Settings.TARGET_SIZE_RANGE_IN_PIXELS[0]) ** 2
        params.maxArea = (Settings.TARGET_SIZE_RANGE_IN_PIXELS[1]) ** 2

        params.filterByCircularity = Settings.FILTER_BY_CIRCULARITY_ON
        params.minCircularity = Settings.MINIMUM_CIRCULARITY
        params.maxCircularity = Settings.MAXIMUM_CIRCULARITY

        params.filterByConvexity = Settings.FILTER_BY_CONVEXITY_ON
        params.minConvexity = Settings.MINIMUM_CONVEXITY
        params.maxConvexity = Settings.MAXIMUM_CONVEXITY

        params.filterByInertia = Settings.FILTER_BY_INERTIA_ON
        params.minInertiaRatio = Settings.MINIMUM_INERTIA_RATIO
        params.maxInertiaRatio = Settings.MAXIMUM_INERTIA_RATIO

        #Create a detector with the parameters.
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
        	detector = cv2.SimpleBlobDetector(params)
        else :
        	detector = cv2.SimpleBlobDetector_create(params)

        #Detect blobs.
        keypoints = detector.detect(self.cv2_target_map_image)

        """
        Return the coordinates of the top left corners of the blobs and their
        widths and heights with margins around them. The margins are checked so
        that they do not extend out of the bound of the image.
        """
        positive_list = []
        for index in range(len(keypoints)):
            center_x = round(keypoints[index].pt[0])
            center_y = round(keypoints[index].pt[1])
            diameter = round(keypoints[index].size)

            top_left_x = center_x - (diameter / 2)
            top_left_y = center_y - (diameter / 2)

            bottom_right_x = center_x + (diameter / 2)
            bottom_right_y = center_y + (diameter / 2)

            if (top_left_x < 0):
                top_left_x = 0

            if (top_left_y < 0):
                top_left_y = 0

            if (bottom_right_x >= self.pil_target_map_image.width):
                bottom_right_x = self.pil_target_map_image.width - 1

            if (bottom_right_y >= self.pil_target_map_image.height):
                bottom_right_y = self.pil_target_map_image.height - 1

            width = bottom_right_x - top_left_x
            height = bottom_right_y - top_left_y

            positive_list.append((top_left_x, top_left_y, width, height))

        #Show the image with detected blobs circled.
        '''
        image_with_keypoints = cv2.drawKeypoints(image, keypoints, numpy.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        image = Image.fromarray(image_with_keypoints, 'RGB')
        image.show()
        '''

        return positive_list

    def detect_canny_edge_contours(self):
        kernel_size = Settings.KERNEL_SIZE
        minimum_threshold = Settings.CANNY_EDGE_CONTOUR_DETECTOR_MINIMUM_THRESHOLD
        maximum_threshold = Settings.CANNY_EDGE_CONTOUR_DETECTOR_MAXIMUM_THRESHOLD

        blurred_cv2_target_map_image = cv2.GaussianBlur(self.cv2_target_map_image, (kernel_size, kernel_size), 0)
        edge = cv2.Canny(blurred_cv2_target_map_image, minimum_threshold, maximum_threshold)

        _, contours, _= cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        positive_list = []
        for index in range(len(contours)):
            contour = contours[index]

            x, y, w, h = cv2.boundingRect(contour)
            positive_list.append((x, y, w, h))

        return positive_list

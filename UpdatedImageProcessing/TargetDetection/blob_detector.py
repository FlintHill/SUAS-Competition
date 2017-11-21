import cv2
import numpy
import PIL.ImageOps
from matplotlib import pyplot
from PIL import Image
from SyntheticDataset2 import *
from .target_detection_settings import TargetDetectionSettings

class BlobDetector(object):

    """
    The following code and descriptions are adapted from OpenCV:
    """
    def __init__(self, image_path):
        """
        :param image_path: the path of an image
        :param target_size_range_in_pixels: the size range of the targets on the
                                            target map.

        :type image_path: an image file such as JPG and PNG
        :type positive_list: a list two elements, the min and max sizes in
                             pixels.
        """
        self.image_path = image_path
        self.raw_image = Image.open(image_path)
        self.raw_image = self.raw_image.convert("RGB")
        self.minimum_area = TargetDetectionSettings.TARGET_SIZE_RANGE_IN_PIXELS[0]
        self.maximum_area = (TargetDetectionSettings.TARGET_SIZE_RANGE_IN_PIXELS[1]) ** 1.5

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

        #Set up Thresholds. Values are changed in TargetDetectionSettings.
        params.minThreshold = TargetDetectionSettings.MINIMUM_THRESHOLD
        params.maxThreshold = TargetDetectionSettings.MAXIMUM_THRESHOLD

        #Set up filters. Values are changed in TargetDetectionSettings.
        params.filterByArea = TargetDetectionSettings.FILTER_BY_AREA_ON
        params.minArea = self.minimum_area
        params.maxArea = self.maximum_area

        params.filterByCircularity = TargetDetectionSettings.FILTER_BY_CIRCULARITY_ON
        params.minCircularity = TargetDetectionSettings.MINIMUM_CIRCULARITY
        params.maxCircularity = TargetDetectionSettings.MAXIMUM_CIRCULARITY

        params.filterByConvexity = TargetDetectionSettings.FILTER_BY_CONVEXITY_ON
        params.minConvexity = TargetDetectionSettings.MINIMUM_CONVEXITY
        params.maxConvexity = TargetDetectionSettings.MAXIMUM_CONVEXITY

        params.filterByInertia = TargetDetectionSettings.FILTER_BY_INERTIA_ON
        params.minInertiaRatio = TargetDetectionSettings.MINIMUM_INERTIA_RATIO
        params.maxInertiaRatio = TargetDetectionSettings.MAXIMUM_INERTIA_RATIO

        #Create a detector with the parameters.
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
        	detector = cv2.SimpleBlobDetector(params)
        else :
        	detector = cv2.SimpleBlobDetector_create(params)

        #Detect blobs.
        inverted_image = PIL.ImageOps.invert(self.raw_image)
        posterized_image = PIL.ImageOps.posterize(inverted_image, 2)
        image = cv2.cvtColor(numpy.array(posterized_image), cv2.COLOR_RGB2BGR)

        keypoints = detector.detect(image)

        """
        Return the coordinates of the top left corners of the blobs and their
        widths and heights with margins around it. The margins are checked so
        that they do not extend out of the bound of the image.
        """
        blob_list = []
        for index in range(len(keypoints)):
            blob_center_x = round(keypoints[index].pt[0])
            blob_center_y = round(keypoints[index].pt[1])
            blob_diameter = round(keypoints[index].size)

            blob_top_left_x = blob_center_x - blob_diameter
            blob_top_left_y = blob_center_y - blob_diameter

            blob_bottom_right_x = blob_center_x + blob_diameter
            blob_bottom_right_y = blob_center_y + blob_diameter

            if (blob_top_left_x < 0):
                blob_top_left_x = 0

            if (blob_top_left_y < 0):
                blob_top_left_y = 0

            if (blob_bottom_right_x >= self.raw_image.width):
                blob_bottom_right_x = self.raw_image.width - 1

            if (blob_bottom_right_y >= self.raw_image.height):
                blob_bottom_right_y = self.raw_image.height - 1

            blob_width = blob_bottom_right_x - blob_top_left_x
            blob_height = blob_bottom_right_y - blob_top_left_y

            blob_list.append((blob_top_left_x, blob_top_left_y, blob_width, blob_height))

        #Show the image with detected blobs circled.
        """
        image_with_keypoints = cv2.drawKeypoints(image, keypoints, numpy.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        image = Image.fromarray(image_with_keypoints, 'RGB')
        image.show()
        """
        return blob_list

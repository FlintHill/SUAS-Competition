import os
from SyntheticDataset2.ImageCreator.settings import Settings

class TargetDetectionSettings(object):
    LOGGING_ON = True

    TARGET_SIZE_RANGE_IN_PIXELS = Settings.TARGET_SIZE_RANGE_IN_PIXELS
    TARGET_AVERAGE_SIZE = (TARGET_SIZE_RANGE_IN_PIXELS[0] + TARGET_SIZE_RANGE_IN_PIXELS[1]) / 2

    """
    Change thresholds for convering source image to binary images. See
    BlobDetector for more information.
    """
    BLOB_DETECTOR_MINIMUM_THRESHOLD = 10
    BLOB_DETECTOR_MAXIMUM_THRESHOLD = 200

    """
    Filter the blobs based on sizes in pixels squared.
    """
    FILTER_BY_AREA_ON = True

    """
    Filter the blobs based on circularity. 0 <= circularity <= 1. See link in
    BlobDetector for more information.
    """
    FILTER_BY_CIRCULARITY_ON = False
    MINIMUM_CIRCULARITY = 0.2
    MAXIMUM_CIRCULARITY = 1

    """
    Filter the blobs based on convexity. 0 <= convexity <= 1. See link in
    BlobDetector for more information.
    """
    FILTER_BY_CONVEXITY_ON = False
    MINIMUM_CONVEXITY = 0.5
    MAXIMUM_CONVEXITY = 1

    """
    Filter the blobs based on inertia ratio. 0 <= inertia ratio <= 1. See link
    in BlobDetector for more information.
    """
    FILTER_BY_INERTIA_ON = True
    MINIMUM_INERTIA_RATIO = 0.2
    MAXIMUM_INERTIA_RATIO = 1

    #For CannyEdgeContourDetector
    KERNEL_SIZE = 3
    CANNY_EDGE_CONTOUR_DETECTOR_MINIMUM_THRESHOLD = 10
    CANNY_EDGE_CONTOUR_DETECTOR_MAXIMUM_THRESHOLD = 200

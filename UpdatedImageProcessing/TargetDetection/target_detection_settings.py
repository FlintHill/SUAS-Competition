import os
from SyntheticDataset2.ImageCreator.settings import Settings

class TargetDetectionSettings(object):
    TARGET_MAPS_DIRECTORY = "/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps"
    TARGET_MAPS_ANSWERS_DIRECTORY = "/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps_answers"

    NUMBER_OF_TARGET_MAPS = sum(os.path.isfile(os.path.join("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps", f)) for f in os.listdir("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps"))

    TARGET_DETECTION_SAVE_PATH = "/Users/zyin/Desktop/Target Detection"

    TARGET_SIZE_RANGE_IN_PIXELS = Settings.TARGET_SIZE_RANGE_IN_PIXELS

    """
    Change thresholds for convering source image to binary images. See
    BlobDetector for more information.
    """
    MINIMUM_THRESHOLD = 10
    MAXIMUM_THRESHOLD = 200

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

    LOGGING_ON = True

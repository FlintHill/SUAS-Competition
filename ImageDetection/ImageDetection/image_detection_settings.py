class ImageDetectionSettings(object):
    IMAGE_PATH = "/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps/2.jpg"

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
    MINIMUM_CIRCULARITY = 0.3
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
    FILTER_BY_INERTIA_ON = False
    MINIMUM_INERTIA_RATIO = 0.3
    MAXIMUM_INERTIA_RATIO = 1

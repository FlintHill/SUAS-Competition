import cv2
import numpy
import io
import PIL.ImageOps
from matplotlib import pyplot
from PIL import Image
from .target_detection_settings import TargetDetectionSettings

class CannyEdgeContourDetector(object):

    def __init__(self, target_map_image_path):
        self.raw_target_map_image = cv2.imread(target_map_image_path, 0)
        self.kernel_size = TargetDetectionSettings.KERNEL_SIZE
        self.minimum_threshold = TargetDetectionSettings.CANNY_EDGE_CONTOUR_DETECTOR_MINIMUM_THRESHOLD
        self.maximum_threshold = TargetDetectionSettings.CANNY_EDGE_CONTOUR_DETECTOR_MAXIMUM_THRESHOLD

    def detect_canny_edge_contours(self):
        blurred_target_map_image = cv2.GaussianBlur(self.raw_target_map_image, (self.kernel_size, self.kernel_size), 0)
        edge = cv2.Canny(blurred_target_map_image, self.minimum_threshold, self.maximum_threshold)

        _, contours, _= cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_list = []
        for index in range(len(contours)):
            contour = contours[index]

            x, y, w, h = cv2.boundingRect(contour)
            contour_list.append((x, y, w, h))

        return contour_list

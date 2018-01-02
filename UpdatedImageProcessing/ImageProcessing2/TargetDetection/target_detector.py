from PIL import Image
from .target_detection_settings import TargetDetectionSettings
from .blob_detector import BlobDetector
from .canny_edge_contour_detector import CannyEdgeContourDetector
from .false_positive_eliminator import FalsePositiveEliminator
from .automatic_tester import AutomaticTester
from .color_operations import ColorOperations

class TargetDetector(object):

    @staticmethod
    def detect_targets(target_map_image_path):
        """
        Detect the targets for one target map and return all positives.

        :param target_map_image_path: the path to a target map image
        :type target_map_image_path: an image file such as JPG and PNG
        """
        positive_list_1 = BlobDetector(target_map_image_path).detect_blobs()
        positive_list_2 = CannyEdgeContourDetector(target_map_image_path).detect_canny_edge_contours()

        target_map_image = Image.open(target_map_image_path)
        target_map_image = ColorOperations.apply_mean_blur(target_map_image, 3)

        if (len(positive_list_1) > 15):
            positive_list_1 = FalsePositiveEliminator.eliminate_overrepeated_colors(target_map_image, positive_list_1)

        if (len(positive_list_2) > 15):
            positive_list_2 = FalsePositiveEliminator.eliminate_overrepeated_colors(target_map_image, positive_list_2)

        positive_list_1 = FalsePositiveEliminator.eliminate_by_surrounding_color(target_map_image, positive_list_1)
        positive_list_2 = FalsePositiveEliminator.eliminate_by_surrounding_color(target_map_image, positive_list_2)

        positive_list = positive_list_1 + positive_list_2

        eliminate_close_by_targets_result = FalsePositiveEliminator.eliminate_close_by_targets(positive_list)
        positive_list = eliminate_close_by_targets_result[0]
        number_of_close_by_targets = eliminate_close_by_targets_result[1]

        while (number_of_close_by_targets > 0):
            eliminate_close_by_targets_result = FalsePositiveEliminator.eliminate_close_by_targets(positive_list)
            positive_list = eliminate_close_by_targets_result[0]
            number_of_close_by_targets = eliminate_close_by_targets_result[1]

        return positive_list

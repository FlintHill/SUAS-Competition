from .target_detection_settings import TargetDetectionSettings
from .blob_detector import BlobDetector
from .false_positive_eliminator import FalsePositiveEliminator
from .automatic_tester import AutomaticTester

class TargetDetector(object):

    @staticmethod
    def detect_targets(target_map_path):
        """
        Detect the targets for one target map and return all positives.

        :param target_map_path: a directory containing the target map images
        :type target_map_path: a directory
        """
        positive_list = BlobDetector(target_map_path).detect_blobs()

        if (len(positive_list) > 15):
            positive_list = FalsePositiveEliminator.eliminate_overrepeated_colors(target_map_path, positive_list)

        positive_list = FalsePositiveEliminator.eliminate_overlapping_blobs(positive_list)
        positive_list = FalsePositiveEliminator.eliminate_by_surrounding_color(target_map_path, positive_list)
        return positive_list

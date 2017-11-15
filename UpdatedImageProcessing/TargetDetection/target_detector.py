from .target_detection_settings import TargetDetectionSettings
from SyntheticDataset2.ImageCreator.settings import Settings
from .blob_detector import BlobDetector
from .false_positive_eliminator import FalsePositiveEliminator
from .automatic_tester import AutomaticTester

class TargetDetector(object):

    def __init__(self, target_map_path, target_map_answer_path):
        self.target_map_path = target_map_path
        self.target_map_answer_path = target_map_answer_path

    def detect_targets(self):
        positive_list = BlobDetector(self.target_map_path, TargetDetectionSettings.TARGET_SIZE_RANGE_IN_PIXELS).detect_blobs()
        if (len(positive_list) > 15):
            positive_list = FalsePositiveEliminator.eliminate_overrepeated_colors(self.target_map_path, positive_list)
        positive_list = FalsePositiveEliminator.eliminate_overlapping_blobs(positive_list)
        return AutomaticTester(positive_list, self.target_map_answer_path).run_automatic_tester()

import os
from .target_detection_settings import TargetDetectionSettings
from .target_detection_logger import TargetDetectionLogger
from .result_recorder import ResultRecorder
from .target_detector import TargetDetector
from .single_targets_capturer import SingleTargetsCapturer

class SingleTargetMapDetector(object):

    @staticmethod
    def detect_single_target_map(path_to_single_target_map):
        positive_list = TargetDetector.detect_targets(path_to_single_target_map)

        single_target_capturer_results = SingleTargetsCapturer.capture_single_targets(path_to_single_target_map, positive_list)
        single_target_crops = single_target_capturer_results[0]
        list_to_eliminate = single_target_capturer_results[1]

        index_2 = len(list_to_eliminate) - 1
        while(index_2 >= 0):
            positive_list.pop(list_to_eliminate[index_2])
            index_2 -= 1

        json_file = ResultRecorder.record_result(positive_list)

        return [single_target_crops, json_file]

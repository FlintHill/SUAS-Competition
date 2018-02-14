import os
from .settings import Settings
from .detection_result_recorder import DetectionResultRecorder
from .integrated_target_detection_process import IntegratedTargetDetectionProcess
from .integrated_target_capturing_process import IntegratedTargetCapturingProcess

class SingleTargetMapDetector(object):

    @staticmethod
    def detect_single_target_map(target_map_image_path):
        positive_list = IntegratedTargetDetectionProcess.run_integrated_target_detection_process(target_map_image_path)
        capturing_results = IntegratedTargetCapturingProcess.run_integrated_target_capturing_process(target_map_image_path, positive_list)
        single_target_crops = capturing_results[0]
        list_to_eliminate = capturing_results[1]

        index_in_list_to_eliminate = len(list_to_eliminate) - 1
        while(index_in_list_to_eliminate >= 0):
            positive_list.pop(list_to_eliminate[index_in_list_to_eliminate])
            index_in_list_to_eliminate -= 1

        json_file = DetectionResultRecorder.record_detection_result(positive_list)

        return [single_target_crops, json_file]

import os
from .settings import Settings
from .logger import Logger
from .detection_result_recorder import DetectionResultRecorder
from .integrated_target_detection_process import IntegratedTargetDetectionProcess
from .integrated_target_capturing_process import IntegratedTargetCapturingProcess

class MassTargetDetector(object):

    @staticmethod
    def detect_mass_target(path_to_target_maps_folder):
        list_of_crops = []
        list_of_json_files = []
        number_of_target_maps = len(os.listdir(path_to_target_maps_folder))

        for index_in_number_of_target_maps in range(1, number_of_target_maps + 1):
            current_target_map = os.path.join(path_to_target_maps_folder, str(index_of_number_of_target_maps) + ".jpg")

            positive_list = IntegratedTargetDetectionProcess.run_integrated_target_detection_process(current_target_map)
            capturing_results = IntegratedTargetCapturingProcess.run_integrated_target_capturing_process(current_target_map, positive_list)
            single_target_crops = capturing_results[0]
            list_to_eliminate = capturing_results[1]

            index_in_list_to_eliminate = len(list_to_eliminate) - 1
            while(index_in_list_to_eliminate >= 0):
                positive_list.pop(list_to_eliminate[index_in_list_to_eliminate])
                index_in_list_to_eliminate -= 1

            json_file = DetectionResultRecorder.record_detection_result(positive_list)

            list_of_crops.append(single_target_crops)
            list_of_json_files.append(json_file)

            Logger.log("Detection for Target Map " + str(index_of_number_of_target_maps) + " Completed")

        return [list_of_crops, list_of_json_files]

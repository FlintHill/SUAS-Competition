import os.path
from .target_detector import TargetDetector
from .target_detection_settings import TargetDetectionSettings

class MassTargetDetector(object):

    @staticmethod
    def run_mass_target_detector():
        number_of_target_maps = sum(os.path.isfile(os.path.join(TargetDetectionSettings.TARGET_MAPS_DIRECTORY, f)) for f in os.listdir(TargetDetectionSettings.TARGET_MAPS_DIRECTORY))
        true_positives_count = 0
        false_positives_count = 0
        false_positives_list = []

        for index in range(1, number_of_target_maps + 1):
            current_target_map = TargetDetectionSettings.TARGET_MAPS_DIRECTORY + "/" + str(index) + ".jpg"
            current_target_map_answers = TargetDetectionSettings.TARGET_MAPS_ANSWERS_DIRECTORY + "/" + str(index) + ".json"

            combo_positive_list = TargetDetector(current_target_map, current_target_map_answers).detect_targets()
            true_positives_count += len(combo_positive_list[0])
            false_positives_count += len(combo_positive_list[1])

            if (len(combo_positive_list[1]) > 0):
                false_positives_list.append([index, combo_positive_list[1]])

        print str(float(true_positives_count) / (float(number_of_target_maps) * 10) * 100) + "%"
        print str(false_positives_count)
        print false_positives_list

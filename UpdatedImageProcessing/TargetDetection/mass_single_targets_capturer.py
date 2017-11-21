from .target_detector import TargetDetector
from .automatic_tester import AutomaticTester
from .single_target_capturer import SingleTargetCapturer
from .target_detection_settings import TargetDetectionSettings

class MassSingleTargetsCapturer(object):

    @staticmethod
    def capture_mass_single_targets():
        for index in range(1, TargetDetectionSettings.NUMBER_OF_TARGET_MAPS + 1):
            current_target_map = TargetDetectionSettings.TARGET_MAPS_DIRECTORY + "/" + str(index) + ".jpg"
            current_target_map_answers = TargetDetectionSettings.TARGET_MAPS_ANSWERS_DIRECTORY + "/" + str(index) + ".json"

            positive_list = TargetDetector.detect_targets(current_target_map)
            combo_positive_list = AutomaticTester.run_automatic_tester(positive_list, current_target_map_answers)

            true_positive_list = combo_positive_list[0]

            for index_2 in range(len(true_positive_list)):
                SingleTargetCapturer.capture_single_target(current_target_map, true_positive_list[index_2])

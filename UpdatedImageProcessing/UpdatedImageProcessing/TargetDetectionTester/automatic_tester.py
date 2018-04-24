import os
import json
from .target_detection_tester_settings import TargetDetectionTesterSettings
from .target_detection_tester_logger import TargetDetectionTesterLogger

class AutomaticTester(object):

    @staticmethod
    def run_automatic_tester():
        """
        Compare the target detection result with the answers of the target map
        and return lists of true and false positives.
        """
        number_of_target_maps = len(os.listdir(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_JSON_FILE_SAVE_PATH))
        overall_true_positive_count = 0
        overall_false_positive_count = 0
        overall_target_count = 0

        for index_0 in range(number_of_target_maps):

            answer_sheet = json.load(open(os.path.join(TargetDetectionTesterSettings.TARGET_MAP_ANSWER_SHEET_PATH, str(index_0 + 1) + ".json")))
            answer_list = []

            for index_1 in range(len(answer_sheet["targets"])):
                answer_list.append((answer_sheet["targets"][index_1]["target_center_coordinates"][0], answer_sheet["targets"][index_1]["target_center_coordinates"][1]))
            overall_target_count += len(answer_list)

            target_detection_result = json.load(open(os.path.join(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_JSON_FILE_SAVE_PATH, str(index_0 + 1) + ".json")))
            result_list = []

            for index_2 in range(len(target_detection_result["image_processing_results"])):
                result_list.append((target_detection_result["image_processing_results"][index_2]["target_location"][0] + (target_detection_result["image_processing_results"][index_2]["target_location"][2] / 2), target_detection_result["image_processing_results"][index_2]["target_location"][1] + (target_detection_result["image_processing_results"][index_2]["target_location"][3] / 2)))

            current_true_positive_count = 0
            current_false_positive_count = 0
            banned_index_list = []

            for index_3 in range(len(answer_list)):
                true_positive_found = False

                for index_4 in range(len(result_list)):
                    is_index_4_banned = False

                    for index_5 in range(len(banned_index_list)):
                        if (index_4 == banned_index_list[index_5]):
                            is_index_4_banned = True

                    if (is_index_4_banned == True):
                        continue

                    correct_target_center_x = answer_list[index_3][0]
                    correct_target_center_y = answer_list[index_3][1]

                    detected_target_center_x = result_list[index_4][0]
                    detected_target_center_y = result_list[index_4][1]

                    if ((abs(correct_target_center_x - detected_target_center_x) <= 20) and (abs(correct_target_center_y - detected_target_center_y) <= 20)):
                        current_true_positive_count += 1
                        banned_index_list.append(index_4)
                        true_positive_found = True
                        continue

            current_false_positive_count = len(result_list) - current_true_positive_count

            overall_true_positive_count += current_true_positive_count
            overall_false_positive_count += current_false_positive_count

        percentage = 100 * float(overall_true_positive_count) / (overall_target_count)

        TargetDetectionTesterLogger.log("--------------------------------------------------")
        TargetDetectionTesterLogger.log("Total True Positive Count: " + str(overall_true_positive_count))
        TargetDetectionTesterLogger.log("Total False Positive Count: " + str(overall_false_positive_count))
        TargetDetectionTesterLogger.log("Percentage of Successfully Detected Targets: " + str(percentage) + "%")
        TargetDetectionTesterLogger.log("--------------------------------------------------")

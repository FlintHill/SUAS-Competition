import os
import json
import timeit
from ..integrated_image_processing import IntegratedImageProcessing
from ..Classifiers import *
from .settings import Settings
from .logger import Logger

class IntegratedImageProcessingTester(object):

    @staticmethod
    def complete_integrated_image_processing():
        if (os.path.isdir(Settings.IMAGE_PROCESSING_REPORT_SAVE_PATH)):
            raise Exception("Cannot create Image Processing Report Save Path: Save directory already exists")
        os.mkdir(Settings.IMAGE_PROCESSING_REPORT_SAVE_PATH)

        if (os.path.isdir(Settings.IMAGE_SAVE_PATH)):
            raise Exception("Cannot create Image Save Path: Save directory already exists")
        os.mkdir(Settings.IMAGE_SAVE_PATH)

        if (os.path.isdir(Settings.JSON_SAVE_PATH)):
            raise Exception("Cannot create Json Save Path: Save directory already exists")
        os.mkdir(Settings.JSON_SAVE_PATH)

        IntegratedImageProcessing.run_integrated_image_processing(Settings.TARGET_MAP_PATH, Settings.IMAGE_SAVE_PATH, Settings.JSON_SAVE_PATH)

    @staticmethod
    def run_integrated_image_processing_tester():
        """
        Compare the image processing result with the answers of the target map
        and print out the results.
        """
        number_of_target_maps = len(os.listdir(Settings.JSON_SAVE_PATH))

        overall_true_positive_count = 0
        overall_false_positive_count = 0

        true_shape_count = 0
        false_shape_count = 0

        true_shape_color_count = 0
        false_shape_color_count = 0

        true_letter_color_count = 0
        false_letter_color_count = 0

        overall_target_count = 0

        for index_0 in range(number_of_target_maps):

            answer_sheet = json.load(open(os.path.join(Settings.TARGET_MAP_ANSWER_SHEET_PATH, str(index_0 + 1) + ".json")))
            answer_list = []

            for index_1 in range(len(answer_sheet["targets"])):
                answer_list.append((answer_sheet["targets"][index_1]))

            overall_target_count += len(answer_list)

            target_detection_result = json.load(open(os.path.join(Settings.JSON_SAVE_PATH, str(index_0 + 1) + ".jpg.json")))
            result_list = []

            for index_2 in range(len(target_detection_result["image_processing_results"])):
                result_list.append((target_detection_result["image_processing_results"][index_2]))

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

                    if is_index_4_banned == True:
                        continue

                    correct_target_center_x = answer_list[index_3]["target_center_coordinates"][0]
                    correct_target_center_y = answer_list[index_3]["target_center_coordinates"][1]

                    detected_target_center_x = result_list[index_4]["target_location"][0]
                    detected_target_center_y = result_list[index_4]["target_location"][1]

                    if (abs(correct_target_center_x - detected_target_center_x) <= 20) and (abs(correct_target_center_y - detected_target_center_y) <= 20):
                        current_true_positive_count += 1
                        banned_index_list.append(index_4)
                        true_positive_found = True

                        current_target_shape = answer_list[index_3]["shape_type"]
                        detected_target_shape = result_list[index_4]["target_shape_type"]

                        current_target_shape_color = ColorClassifier().convert_rgba_to_color_name(answer_list[index_3]["shape_color"])
                        detected_target_shape_color = result_list[index_4]["target_shape_color"]

                        current_target_letter_color = ColorClassifier().convert_rgba_to_color_name(answer_list[index_3]["alphanumeric_color"])
                        detected_target_letter_color = result_list[index_4]["target_letter_color"]

                        if current_target_shape == detected_target_shape:
                            true_shape_count += 1
                        else:
                            false_shape_count += 1

                        if current_target_shape_color == detected_target_shape_color:
                            true_shape_color_count += 1
                        else:
                            false_shape_color_count += 1

                        if current_target_letter_color == detected_target_letter_color:
                            true_letter_color_count += 1
                        else:
                            false_letter_color_count += 1

                        continue

            current_false_positive_count = len(result_list) - current_true_positive_count

            overall_true_positive_count += current_true_positive_count
            overall_false_positive_count += current_false_positive_count

        target_detection_percentage = 100 * float(overall_true_positive_count) / (overall_target_count)
        overall_shape_detection_percentage = 100 * float(true_shape_count) / (overall_target_count)
        target_detection_based_shape_detection_percentage = 100 * float(true_shape_count) / (overall_true_positive_count)
        overall_shape_color_detection_percentage = 100 * float(true_shape_color_count) / (overall_target_count)
        target_detection_based_shape_color_detection_percentage = 100 * float(true_shape_color_count) / (overall_true_positive_count)
        overall_letter_color_detection_percentage = 100 * float(true_letter_color_count) / (overall_target_count)
        target_detection_based_letter_color_detection_percentage = 100 * float(true_letter_color_count) / (overall_true_positive_count)

        Logger.log("--------------------------------------------------")
        Logger.log("Total True Positive Count: " + str(overall_true_positive_count))
        Logger.log("Total False Positive Count: " + str(overall_false_positive_count))
        Logger.log("Percentage of Successfully Detected Targets: " + str(target_detection_percentage) + "%")
        Logger.log("--------------------------------------------------")
        Logger.log("Total True Shape Count: " + str(true_shape_count))
        Logger.log("Total False Shape Count: " + str(false_shape_count))
        Logger.log("Overall Percentage of Successfully Detected Shape: " + str(overall_shape_detection_percentage) + "%")
        Logger.log("Percentage of Successfully Detected Shape based on Target Detection Result: " + str(target_detection_based_shape_detection_percentage) + "%")
        Logger.log("--------------------------------------------------")
        Logger.log("Total True Shape Color Count: " + str(true_shape_color_count))
        Logger.log("Total False Shape Color Count: " + str(false_shape_color_count))
        Logger.log("Overall Percentage of Successfully Detected Shape Color: " + str(overall_shape_color_detection_percentage) + "%")
        Logger.log("Percentage of Successfully Detected Shape Color based on Target Detection Result: " + str(target_detection_based_shape_color_detection_percentage) + "%")
        Logger.log("--------------------------------------------------")
        Logger.log("Total True Letter Color Count: " + str(true_letter_color_count))
        Logger.log("Total False Letter Color Count: " + str(false_letter_color_count))
        Logger.log("Overall Percentage of Successfully Detected Letter Color: " + str(overall_letter_color_detection_percentage) + "%")
        Logger.log("Percentage of Successfully Detected Letter Color based on Target Detection Result: " + str(target_detection_based_letter_color_detection_percentage) + "%")
        Logger.log("--------------------------------------------------")

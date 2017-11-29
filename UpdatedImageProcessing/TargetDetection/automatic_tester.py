import json
from .target_detection_settings import TargetDetectionSettings
from .target_detection_logger import TargetDetectionLogger

class AutomaticTester(object):

    @staticmethod
    def run_automatic_tester(positive_list, answer_sheet_path):
        """
        Compare the positive_list with the answers of the a target map and
        return the list of the true and false positives.

        :param positive_list: the list holding the information of the blobs.
        :param answer_sheet_path: the path to the json file of the answers of
                                     the background image under detection.

        :type positive_list: a list of four-tuples containing four elements for each
                             blob: (x, y, length, width)
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        :type answer_sheet_path: a json file
        """
        answer_sheet = json.load(open(answer_sheet_path))

        true_positive_list = []
        false_positive_list = []
        for index_1 in range(len(positive_list)):
            true_positive_found = False
            for index_2 in range(len(answer_sheet["targets"])):
                blob_center_x = positive_list[index_1][0] + (positive_list[index_1][2] / 2)
                blob_center_y = positive_list[index_1][1] + (positive_list[index_1][3] / 2)
                target_center_x = answer_sheet["targets"][index_2]["target_center_coordinates"][0]
                target_center_y = answer_sheet["targets"][index_2]["target_center_coordinates"][1]

                if ((abs(blob_center_x - target_center_x) <= 20) and (abs(blob_center_y - target_center_y) <= 20)):
                    true_positive_list.append(positive_list[index_1])
                    true_positive_found = True
            if (true_positive_found == False):
                false_positive_list.append(positive_list[index_1])

        return [true_positive_list, false_positive_list]

    @staticmethod
    def save_result(true_positive_list, false_positive_list, index_number):
        """
        Save the result of the automatic test to
        TargetDetectionSettings.TARGET_DETECTION_REPORT_SAVE_PATH.

        :param true_positive_list: the list holding the information of the
                                   correctly detected blobs
        :param false_positive_list: the list holding the information of the
                                    incorrectly detected blobs
        :param index_number: the number to be used to serialize the target map
                             reports

        :type true_positive_list: a list of four-tuples containing four elements
                                  for each blob: (x, y, length, width)
        :type false_positive_list: a list of four-tuples containing four elements
                                   for each blob: (x, y, length, width)
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        :type index_number: int
        """
        data = {}

        data["true_positive_list"] = []
        for index in range(len(true_positive_list)):
            data["true_positive_list"].append(true_positive_list[index])

        data["false_positive_list"] = []
        for index in range(len(false_positive_list)):
            data["false_positive_list"].append(false_positive_list[index])

        data["true_positive_count"] = []
        data["true_positive_count"].append(len(true_positive_list))

        data["false_positive_count"] = []
        data["false_positive_count"].append(len(false_positive_list))

        with open(TargetDetectionSettings.TARGET_DETECTION_REPORT_SAVE_PATH + "/Target Map Reports/" + str(index_number) + ".json", 'w') as outfile:
            json.dump(data, outfile, indent = 4)

    @staticmethod
    def report_result():
        total_true_positive_count = 0
        total_false_positive_count = 0

        for index in range(1, TargetDetectionSettings.NUMBER_OF_TARGET_MAPS + 1):
            target_detection_report = json.load(open(TargetDetectionSettings.TARGET_DETECTION_REPORT_SAVE_PATH + "/Target Map Reports/" + str(index) + ".json"))

            total_true_positive_count += target_detection_report["true_positive_count"][0]
            total_false_positive_count += target_detection_report["false_positive_count"][0]

        percentage = 100 * total_true_positive_count / (TargetDetectionSettings.NUMBER_OF_TARGET_MAPS * TargetDetectionSettings.NUMBER_OF_TARGETS_ON_EACH_MAP)

        TargetDetectionLogger.log("--------------------------------------------------")
        TargetDetectionLogger.log("Total True Positive Count: " + str(total_true_positive_count))
        TargetDetectionLogger.log("Total False Positive Count: " + str(total_false_positive_count))
        TargetDetectionLogger.log("Percentage of Successfully Detected Targets: " + str(percentage) + "%")
        TargetDetectionLogger.log("--------------------------------------------------")

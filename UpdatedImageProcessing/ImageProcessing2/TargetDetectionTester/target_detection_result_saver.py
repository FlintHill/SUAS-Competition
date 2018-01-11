import os
import json
from .target_detection_tester_settings import TargetDetectionTesterSettings

class TargetDetectionResultSaver(object):

    @staticmethod
    def save_target_detection_result(combo_target_detection_result_list):
        list_of_crops = combo_target_detection_result_list[0]
        list_of_json_files = combo_target_detection_result_list[1]

        if (os.path.isdir(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_SAVE_PATH)):
            raise Exception("Cannot create Target_Detection_Report: Save directory already exists")
        os.mkdir(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_SAVE_PATH)

        if (os.path.isdir(os.path.join(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_SAVE_PATH, "Json_Files"))):
            raise Exception("Cannot create Target_Map_Reports: Save directory already exists")
        os.mkdir(os.path.join(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_SAVE_PATH, "Json_Files"))

        if (os.path.isdir(os.path.join(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_SAVE_PATH, "Single_Target_Crops"))):
            raise Exception("Cannot create Single_Target_Crops: Save directory already exists")
        os.mkdir(os.path.join(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_SAVE_PATH, "Single_Target_Crops"))

        for index_1 in range(len(list_of_crops)):
            for index_2 in range(len(list_of_crops[index_1])):
                list_of_crops[index_1][index_2].save(os.path.join(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_SAVE_PATH, "Single_Target_Crops", str(index_1 + 1) + "-" + str(index_2 + 1) + ".png"))

        for index_3 in range(len(list_of_json_files)):
            with open(os.path.join(TargetDetectionTesterSettings.TARGET_DETECTION_REPORT_SAVE_PATH, "Json_Files", str(index_3 + 1) + ".json"), 'w') as fp:
                json.dump(list_of_json_files[index_3], fp, indent=4)

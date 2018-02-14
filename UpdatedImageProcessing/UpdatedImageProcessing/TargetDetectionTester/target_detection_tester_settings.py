import os

class TargetDetectionTesterSettings(object):
    LOGGING_ON = True
    
    """
    This path contains the following paths for saving single target crops and
    json fils.
    """
    TARGET_DETECTION_REPORT_SAVE_PATH = os.path.expanduser("~/Desktop/Target_Detection_Report")

    """
    the path to the directory that stores the crops of single targets obtained
    through the target detection process.
    """
    TARGET_DETECTION_REPORT_SINGLE_CROP_SAVE_PATH = os.path.join(TARGET_DETECTION_REPORT_SAVE_PATH, "Single_Target_Crops")

    """
    the path to the directory that stores the json files each holding the
    detected information of the targets on its corresponding target map.
    """
    TARGET_DETECTION_REPORT_JSON_FILE_SAVE_PATH = os.path.join(TARGET_DETECTION_REPORT_SAVE_PATH, "Json_Files")

    """
    the path to the directory that stores the json file each holding the
    correct information of the targets on to its corresponding target map.
    """
    TARGET_MAP_ANSWER_SHEET_PATH = os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps_answers")

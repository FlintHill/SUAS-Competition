import os

class Settings(object):
    LOGGING_ON = True

    """
    This path contains the target maps to be used for image processing.
    """
    TARGET_MAP_PATH = os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps")
    #TARGET_MAP_PATH = os.path.expanduser("~/Desktop/manual_dataset/target_map")

    """
    This path contains the following paths for saving single target crops and
    json fils.
    """
    IMAGE_PROCESSING_REPORT_SAVE_PATH = os.path.expanduser("~/Desktop/Image_Processing_Report")

    """
    the path to the directory that stores the crops of single targets obtained
    through the target detection process.
    """
    IMAGE_SAVE_PATH = os.path.join(IMAGE_PROCESSING_REPORT_SAVE_PATH, "Images")

    """
    the path to the directory that stores the json files each holding the
    detected information of the targets on its corresponding target map.
    """
    JSON_SAVE_PATH = os.path.join(IMAGE_PROCESSING_REPORT_SAVE_PATH, "Jsons")

    """
    the path to the directory that stores the json file each holding the
    correct information of the targets on to its corresponding target map.
    """
    TARGET_MAP_ANSWER_SHEET_PATH = os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps_answers")
    #TARGET_MAP_ANSWER_SHEET_PATH = os.path.expanduser("~/Desktop/manual_dataset/target_map_answers")

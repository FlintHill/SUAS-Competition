import os

class Settings(object):
    FONT_TYPE = "UpdatedSyntheticDataset/data/fonts/GothamBold.ttf"
    BACKGROUND_DIRECTORY_PATH = os.path.expanduser("~/Desktop/Synthetic_Dataset/Backgrounds")

    SAVE_PATH = os.path.expanduser("~/Desktop/Synthetic_Dataset")
    ANSWERS_DIRECTORY = "/Answers"

    PPSI = 1.5

    SINGLE_TARGET_SIZE_IN_INCHES = 24.0
    SINGLE_TARGET_SIZE_IN_PIXELS = int(SINGLE_TARGET_SIZE_IN_INCHES * PPSI)

    TARGET_SIZE_RANGE_IN_INCHES = [12.0, 48.0]
    TARGET_SIZE_RANGE_IN_PIXELS = [int(TARGET_SIZE_RANGE_IN_INCHES[0]) * PPSI, int(TARGET_SIZE_RANGE_IN_INCHES[1]) * PPSI]

    TARGET_GENERATION_SIZE_IN_PIXELS = 200

    #See SpecifiedTarget
    SINGLE_TARGET_PROPORTIONALITY = 2.5
    PROPORTIONALITY_RANGE = [1.5, 2.5]
    #See ImageResizer
    PIXELIZATION_LEVEL = 10

    NOISE_LEVEL = 2

    LOGGING_ON = True

class Settings(object):
    FONT_TYPE = "UpdatedSyntheticDataset/data/fonts/GothamBold.ttf"
    BACKGROUND_DIRECTORY_PATH = "/Users/zyin/Desktop/Synthetic Dataset/Backgrounds"

    SAVE_PATH = "/Users/vtolpegin/Desktop"
    ANSWERS_DIRECTORY = "/SyntheticDataset"

    PPSI = 10

    SINGLE_TARGET_SIZE_IN_INCHES = 24.0
    SINGLE_TARGET_SIZE_IN_PIXELS = int(SINGLE_TARGET_SIZE_IN_INCHES * PPSI)

    TARGET_SIZE_RANGE_IN_INCHES = [12.0, 48.0]
    TARGET_SIZE_RANGE_IN_PIXELS = [int(TARGET_SIZE_RANGE_IN_INCHES[0]) * PPSI, int(TARGET_SIZE_RANGE_IN_INCHES[1]) * PPSI]

    TARGET_GENERATION_SIZE_IN_PIXELS = 200

    SINGLE_TARGET_PROPORTIONALITY = 2.5
    PROPORTIONALITY_RANGE = [1.5, 2.5]
    """See SpecifiedTarget"""

    PIXELIZATION_LEVEL = 10
    """See ImageResizer"""

    NOISE_LEVEL = 2

    LOGGING_ON = True

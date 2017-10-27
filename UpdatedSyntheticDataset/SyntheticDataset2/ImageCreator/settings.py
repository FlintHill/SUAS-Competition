class Settings(object):
    FONT_TYPE = "UpdatedSyntheticDataset/data/fonts/Blockletter.otf"
    BACKGROUND_DIRECTORY = "/Users/zyin/Desktop/Synthetic Dataset/Backgrounds"

    IMAGE_SAVING_PATH = "/Users/zyin/Desktop/Synthetic Dataset/Answers/Resultant Images"
    TEXT_SAVING_PATH = "/Users/zyin/Desktop/Synthetic Dataset/Answers/Resultant Texts"

    PPSI = 10

    SINGLE_TARGET_SIZE_IN_INCHES = 24.0
    SINGLE_TARGET_SIZE_IN_PIXELS = int(SINGLE_TARGET_SIZE_IN_INCHES * PPSI)

    TARGET_SIZE_RANGE_IN_INCHES = [12.0, 48.0]
    TARGET_SIZE_RANGE_IN_PIXELS = [int(TARGET_SIZE_RANGE_IN_INCHES[0]) * PPSI, int(TARGET_SIZE_RANGE_IN_INCHES[1]) * PPSI]

    TARGET_GENERATION_SIZE_IN_PIXELS = 1000

    SINGLE_TARGET_PROPORTIONALITY = 2.5
    PROPORTIONALITY_RANGE = [1.5, 2.5]
    """See SpecifiedTargetCreator"""

    PIXELIZATION_LEVEL = 0
    """See ImageResizer"""

    NOISE_LEVEL = 0

    LOGGING_ON = True

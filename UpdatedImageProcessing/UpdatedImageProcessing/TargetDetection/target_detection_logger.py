from .target_detection_settings import TargetDetectionSettings

class TargetDetectionLogger(object):

    @staticmethod
    def log(message):
        if TargetDetectionSettings.LOGGING_ON:
            print(message)

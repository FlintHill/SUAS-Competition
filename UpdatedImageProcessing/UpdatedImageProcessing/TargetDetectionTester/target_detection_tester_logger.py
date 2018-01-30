from .target_detection_tester_settings import TargetDetectionTesterSettings

class TargetDetectionTesterLogger(object):

    @staticmethod
    def log(message):
        if TargetDetectionTesterSettings.LOGGING_ON:
            print(message)

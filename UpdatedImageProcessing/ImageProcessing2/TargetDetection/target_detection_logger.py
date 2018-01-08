from .target_detection_settings import TargetDetectionSettings

class TargetDetectionLogger(object):

    @staticmethod
    def log(message):
        if TargetDetectionSettings.LOGGING_ON:
            print(message)

    @staticmethod
    def format_time_report(time_in_seconds):
        minutes = int(time_in_seconds / 60)
        seconds = time_in_seconds - (minutes * 60)
        print str(minutes) + "min " + str(seconds) + "s"

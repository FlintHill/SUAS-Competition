from .settings import ImageProcessingClassifierSettings

class Logger(object):

    @staticmethod
    def log(message):
        if ImageProcessingClassifierSettings.LOGGING_ON:
            print(message)

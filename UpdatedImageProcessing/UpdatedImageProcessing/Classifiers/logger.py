from .settings import ImgProcSettings

class Logger(object):

    @staticmethod
    def log(message):
        if ImgProcSettings.LOGGING_ON:
            print(message)

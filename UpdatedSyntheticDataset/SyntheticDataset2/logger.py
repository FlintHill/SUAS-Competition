from .ImageCreater.settings import Settings

class Logger(object):

    @staticmethod
    def log(message):
        if Settings.LOGGING_ON:
            print(message)

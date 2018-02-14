from .settings import Settings

class Logger(object):

    @staticmethod
    def log(message):
        if Settings.LOGGING_ON:
            print(message)

    @staticmethod
    def format_time_report(time_in_seconds):
        minutes = int(time_in_seconds / 60)
        seconds = time_in_seconds - (minutes * 60)
        print str(minutes) + " minute(s) " + str(seconds) + " second(s)"

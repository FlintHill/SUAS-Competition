import cv2


class PixhawkLogParser:
    """
    Parses Pixhawk's logs to identify vital information to the mission.
    """

    def __init__(self):
        self.log = ""

    def parse(self, logfile, condition_to_trigger):
        """
        Parse the log files looking for the following components:
        1) GPS location
        2) Heading

        The method uses the condition "condition_to_trigger" to determine
        when the above data needs to be captured. It grabs data when
        appropriate, adds it to a list of dictionaries, and finally returns
        that list.
        """
        # Returning the parsed log data
        return [{}]

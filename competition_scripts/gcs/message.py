class Message:
    """
    Simple container class to send messages through multiprocessing
    pipes
    """

    def __init__(self, message):
        """
        Initialize a Message object

        :param message: Message to send through the pipe
        """
        self.message = message

    def get_message(self):
        """
        Returns the message
        """
        return self.message

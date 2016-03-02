class ADLCParser:
    """
    General class for processing ADLC-related images
    """

    def __init__(self):
        pass

    def simple_parse(self, image):
        """
        Returns true/false whether an in-depth parse should be applied. This
        method only does a couple of quick checks to remove images where it is
        clear there are no targets.
        """
        # @TODO: Implement simple parsing

        return True

    def parse(self, image):
        """
        Parses the given image to identify potential ADLC targets. Returns a
        list of possible targets.
        """
        # @TODO: Implement parsing

        pass

    def identify_characteristics(self, target):
        """
        Identifies the characteristics of the target "target" and returns
        them as a dictionary object
        """
        # @TODO: Implement characteristic identification

        return {}

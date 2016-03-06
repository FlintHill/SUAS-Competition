from SUASImageParser.ADLC import ADLCParser

import os


class ImageParser:
    """
    Main image parsing class for the SUASImageParser library. This handles the
    actual interface between the parsers, optimizers, and the user.
    """

    def __init__(self, **kwargs):
        # Initialize parsing settings
        self.mode = kwargs.get("mode", "")
        self.debug = kwargs.get("debug", False)

        # Initializing parsers
        self.adlc_parser = ADLCParser()
        self.adlc_parser.set_debug(self.debug)

        # Initialize optimizers
        # @TODO: Initialize optimizers

        # Optimize parameters
        self.optimize()

    def parse(self, filename):
        """
        Parses the image "filename" and returns the generated image
        """
        if self.mode == "ADLC":
            targets, characteristics = self.adlc_parser.parse(filename)
            return targets

        return None

    def optimize(self):
        """
        Optimize the parser using gold standard data
        """
        # Initializing data folder (containing optimization data) if it
        #   doesn't exist
        if not os.path.exists("generated_data"):
            os.mkdir("generated_data")

        # @TODO: Implement optimization for each gold standard available

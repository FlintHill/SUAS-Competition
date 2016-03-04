from SUASImageParser.ADLC import ADLCParser

class ImageParser:

    def __init__(self, mode, debug):
        self.mode = mode
        self.debug = debug

        self.adlc_parser = ADLCParser()
        self.adlc_parser.set_debug(self.debug)

    def parse(self, filename):
        """
        Parses the image "filename" and returns the generated image
        """
        if self.mode == "ADLC":
            return self.adlc_parser.parse(filename)

        return None

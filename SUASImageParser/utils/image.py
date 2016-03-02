class Image:
    """
    Interface class to an image
    """

    def __init__(self):
        self.image = None

    def load(self, filename):
        """
        Load an image from a file. Returns a boolean value whether the
        operation succceeds.
        """
        # @TODO: Load an image from a file
        # @TODO: Return true/false based on outcome of loading

    def get_image(self):
        """
        Returns the image as an array of pixels.
        """
        # @TODO: Return the image

    def get_ROI(self, start, end):
        """
        Returns the region of the image as defined by the point
        [start[x], start[y]], [end[x], end[y]]
        """
        # @TODO: Return the ROI

    def set_image(self, image):
        """
        Set the image to "image"
        """
        self.image = image

        return True

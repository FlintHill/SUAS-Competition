import cv2

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
        self.image = cv2.imread(filename)

        return True

    def get_image(self):
        """
        Returns the image
        """
        return self.image

    def get_ROI(self, start, end):
        """
        Returns the region of the image as defined by the point
        [start[x], start[y]], [end[x], end[y]]
        """
        return self.image[ start[y] : end[y], start[x] : end[x] ]

    def set_image(self, image):
        """
        Set the image to "image"
        """
        self.image = image

        return True

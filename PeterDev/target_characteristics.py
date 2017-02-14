class TargetCharacteristics:

    def __init__(self, latitude, longitude, orientation, shape, background_color, alphanumeric, alphanumeric_color):
        """
        Initialize

        :param latitude: The latitude of the target
        :param longitude: The longitude of the target
        :param orientation: The orientation of the target
        :param shape: The shape of the target
        :param background_color: The color of the shape
        :param alphanumeric: The alphanumeric on the target
        :param alphanumeric_color: The color of the alphanumeric
        """
        self.latitude = latitude
        self.longitude = longitude
        self.orientation = orientation
        self.shape = shape
        self.background_color = background_color
        self.alphanumeric = alphanumeric
        self.alphanumeric_color = alphanumeric_color

    def get_latitude(self):
        """
        Returns the target's latitude
        """
        return self.latitude

    def get_longitude(self):
        """
        Returns the target's longitude
        """
        return self.longitude

    def get_orientation(self):
        """
        Returns the target's orientation
        """
        return self.orientation

    def get_shape(self):
        """
        Returns the target's shape
        """
        return self.shape

    def get_background_color(self):
        """
        Returns the target's color
        """
        return self.background_color

    def get_alphanumeric(self):
        """
        Returns the alphanumeric
        """
        return self.alphanumeric

    def get_alphanumeric_color(self):
        """
        Returns the color of the alphanumeric
        """
        return self.alphanumeric_color

class Target:

    def __init__(self, crop, characteristics):
        """
        Initialize

        :param crop: The cropped target
        :param characteristics: The characteristics of the cropped target
        """
        self.crop = crop
        self.characteristics = characteristics

    def get_crop(self):
        """
        Return the cropped target
        """
        return self.crop

    def get_characteristics(self):
        """
        Return the cropped target's characteristics
        """
        return self.characteristics

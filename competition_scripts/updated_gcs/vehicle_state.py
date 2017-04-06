from location_data import LocationData

class VehicleState(LocationData):

    def __init__(self, lat, lon, alt, direction, groundspeed):
        """
        Initialize

        :param lat: The latitude of the vehicle
        :type lat: float
        :param lon: The longitude of the vehicle
        :type lon: float
        :param alt: The altitude of the vehicle
        :type alt: float
        :param direction: The direction of the vehicle
        :type direction: float
        :param groundspeed: The groundspeed of the vehicle
        :type groundspeed: float
        """
        super(self, VehicleState).__init__(lat, lon, alt)

        self.direction = direction
        self.groundspeed = groundspeed

    def get_direction(self):
        """
        Return the direction
        """
        return self.direction

    def get_groundspeed(self):
        """
        Return the groundspeed
        """
        return self.groundspeed

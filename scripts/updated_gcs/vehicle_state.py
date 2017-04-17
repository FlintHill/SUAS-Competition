from location_data import Location

class VehicleState(Location):

    def __init__(self, lat, lon, alt, direction, groundspeed, velocity, obstacle_in_path):
        """
        Initialize

        :param lat: The latitude of the vehicle
        :type lat: float
        :param lon: The longitude of the vehicle
        :type lon: float
        :param alt: The altitude of the vehicle
        :type alt: float
        :param direction: The direction of the vehicle (degrees)
        :type direction: float
        :param groundspeed: The groundspeed of the vehicle
        :type groundspeed: float
        :param velocity: The velocity of the UAV
        :type velocity: Float
        :param obstacle_in_path: Whether an obstacle is in the path of the UAV
        :type obstacle_in_path: Boolean
        """
        super(VehicleState, self).__init__(lat, lon, alt)

        self.direction = direction
        self.velocity = velocity
        self.groundspeed = groundspeed
        self.obstacle_in_path = obstacle_in_path

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

    def get_velocity(self):
        """
        Return the velocity
        """
        return self.velocity

    def get_obstacle_in_path(self):
        """
        Return whether an obstacle is in the path of the UAV
        """
        return self.obstacle_in_path

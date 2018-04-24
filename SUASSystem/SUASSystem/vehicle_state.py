from SUASSystem import Location
from .settings import GCSSettings

class VehicleState(Location):

    def __init__(self, lat, lon, alt, direction, groundspeed, velocity, obstacle_in_path, current_waypoint_number):
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
        :type velocity: Numpy Array
        :param obstacle_in_path: Whether an obstacle is in the path of the UAV
        :type obstacle_in_path: Boolean
        :param current_waypoint_number: The current waypoint the UAV is travelling to
        :type current_waypoint_number: int
        """
        super(VehicleState, self).__init__(lat, lon, alt)

        self.direction = direction
        self.velocity = velocity
        self.groundspeed = groundspeed
        self.obstacle_in_path = obstacle_in_path
        self.current_waypoint_number = current_waypoint_number

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
        magnitude = 0
        for component in self.velocity:
            magnitude += component**2
        magnitude = magnitude**0.5
        #TODO: verify correct units
        magnitude *= GCSSettings.KNOTS_PER_METERS_PER_SECOND

        return magnitude

    def get_obstacle_in_path(self):
        """
        Return whether an obstacle is in the path of the UAV
        """
        return self.obstacle_in_path

    def get_location(self):
        """
        Return the VehicleState object's location
        """
        return Location(self.get_lat(), self.get_lon(), self.get_alt())

    def get_current_waypoint_number(self):
        """
        Return the current waypoint number (current as of the creation of the
        VehicleState object)
        """
        return self.current_waypoint_number

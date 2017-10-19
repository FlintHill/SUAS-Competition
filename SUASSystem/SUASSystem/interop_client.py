from interop import Client
from interop import Telemetry
from interop import Odlc
from .settings import GCSSettings

class InteropClientConverter(object):

    def __init__(self):
        self.client = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)

    def post_telemetry(self, location, heading):
        """
        Post the drone's telemetry information

        :param location: The location to post
        :type location: Location
        :param heading: The UAV's heading
        :type heading: Float
        """
        telem_upload_data = Telemetry(location.get_lat(), location.get_lon(), location.get_alt() + GCSSettings.MSL_ALT, heading)

        self.client.post_telemetry(telem_upload_data)

    def get_obstacles(self):
        """
        Return the obstacles.

        Returned in the format: [StationaryObstacle], [MovingObstacle]
        """
        stationary_obstacles, moving_obstacles = self.client.get_obstacles()

        return stationary_obstacles, moving_obstacles

    def get_active_mission(self):
        """
        Get the active mission and return it. If no missions are active, return
        None

        :return: Active Mission
        :return type: Mission / None
        """
        missions = self.client.get_missions()

        for mission in missions:
            if mission.active:
                return mission

        return None

    def post_standard_target(self, target, image_file_path):
        """
        POST a standard ODLC object to the interoperability server.

        :param target: The ODLC target object
        :type target: JSON, with the form:
        {
            "latitude" : float,
            "longitude" : float,
            "orientation" : string,
            "shape" : string,
            "background_color" : string,
            "alphanumeric" : string,
            "alphanumeric_color" : string,
        }

        :param image_file_path: The OLC target image file name
        :type image_file_path: String

        :return: ID of the posted target
        """
        odlc_target = Odlc(
            type="standard",
            autonomous=False,
            latitude=target["latitude"],
            longitude=target["longitude"],
            orientation=target["orientation"],
            shape=target["shape"],
            background_color=target["background_color"],
            alphanumeric=target["alphanumeric"],
            alphanumeric_color=target["alphanumeric_color"],
            description='Flint Hill School -- ODLC Autonomous Target Submission')

        returned_odlc = self.client.post_odlc(odlc_target)

        with open(image_file_path) as img_file:
            self.client.post_odlc_image(returned_odlc.id, img_file.read())

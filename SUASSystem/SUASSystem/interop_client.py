from __future__ import print_function
from interop import Client
from interop import Telemetry
from time import sleep

class InteropClientConverter:

    def __init__(self, msl_alt, url, username, password):
        self.msl_alt = msl_alt
        self.url = url
        self.username = username
        self.password = password

        self.client = Client(url, username, password)

    def post_telemetry(self, location, heading):
        """
        Post the drone's telemetry information

        :param location: The location to post
        :type location: Location
        :param heading: The UAV's heading
        :type heading: Float
        """
        telem_upload_data = Telemetry(location.get_lat(), location.get_lon(), location.get_alt() + self.msl_alt, heading)

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

    def get_client(self):
        """
        Return the client
        """
        return self.client

    def post_standard_target(self, target, image_file_path):
        """
        POST a standard ODLC object to the interoperability server.

        :param target: The ODLC target object
        :type target: JSON, with the form:
        {
            "location" : GpsPosition,
            "orientation" : Orientation.X,
            "shape" : Shape.X,
            "background_color" : Color.X,
            "alphanumeric" : "X",
            "alphanumeric_color" : Color.X,
        }

        :param image_file_path: The OLC target image file name
        :type image_file_path: String

        :return: ID of the posted target
        """
        with open(image_file_path) as img_file:
            target_img = interop.SimpleUploadedFile('target_img.jpg', img_file.read())

        odlc_target = Odlc(
            odlc_type=interop.OdlcType.standard,
            location=target["location"],
            orientation=target["orientation"],
            shape=target["shape"],
            background_color=target["background_color"],
            alphanumeric=target["alphanumeric"],
            alphanumeric_color=target["alphanumeric_color"],
            description='Flint Hill School -- ODLC Autonomous Target Submission')

        returned_odlc = self.client.post_odlc(odlc_target)
        self.client.post_odlc_image(returned_odlc.id, target_img)

        return returned_odlc.id

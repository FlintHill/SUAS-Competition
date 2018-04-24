from interop import Client
from interop import Telemetry
from interop import Odlc
from .settings import GCSSettings
from time import sleep
from time import time
from requests.exceptions import ConnectionError

class InteropClientConverter(object):

    def __init__(self):
        self.client = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)

    def post_telemetry(self, location, heading):
        """
        Post the drone's telemetry information.

        :param location:    The location to post.
        :type location:     Location
        :param heading:     The UAV's heading.
        :type heading:      Float
        """
        # TODO: remove after testing
        # telem_upload_data = Telemetry(location.get_lat(), location.get_lon(), location.get_alt() + GCSSettings.MSL_ALT, heading)
        missing_data = True

        while missing_data:
            try:
                telem_upload_data = Telemetry(location.get_lat(), location.get_lon(), location.get_alt() + GCSSettings.MSL_ALT, heading)
                missing_data = False
            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE)

                try:
                    self.client = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                except:
                    print("Failed to connect to Interop., retrying...")

        self.client.post_telemetry(telem_upload_data)

    def get_obstacles(self):
        """
        Return the obstacles.

        :return: [StationaryObstacle], [MovingObstacle]
        """
        missing_data = True

        while missing_data:
            try:
                stationary_obstacles, moving_obstacles = self.client.get_obstacles()
                missing_data = False
            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE) # todo: 0.5

                try:
                    self.client = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                except:
                    print("Failed to connect to Interop., retrying...")

        return stationary_obstacles, moving_obstacles

    def get_active_mission(self):
        """
        Get the active mission and return it. If no missions are active,
        then this function will return None.

        :return:        Active Mission.
        :return type:   Mission / None
        """
        # TODO: remove after testing
        #missions = self.client.get_missions()

        missing_data = True

        while missing_data:
            try:
                missions = self.client.get_missions()
                missing_data = False
            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE) # todo: 0.5

                try:
                    self.client = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                except:
                    print("Failed to connect to Interop., retrying...")

        for mission in missions:
            if mission.active:
                return mission

        return None

    def post_manual_standard_target(self, target, image_file_path):
        """
        POST a standard ODLC object to the interoperability server.

        :param target: The ODLC target object.
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

        :param image_file_path: The ODLC target image file name.
        :type image_file_path:  String

        :return: ID of the posted target.
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
            description='Flint Hill School -- ODLC Standard Target Submission')

        # TODO: remove after testing
        #returned_odlc = self.client.post_odlc(odlc_target)

        missing_data = True

        while missing_data:
            try:
                returned_odlc = self.client.post_odlc(odlc_target)
                missing_data = False
            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE) # todo: 0.5

                try:
                    self.client = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                except:
                    print("Failed to connect to Interop, retrying...")

        with open(image_file_path) as img_file:
            self.client.post_odlc_image(returned_odlc.id, img_file.read())

    def post_manual_emergent_target(self, target, image_file_path):
        """
        POST an emergent ODLC object to the interoperability server.

        :param target: The ODLC target object.
        :type target: JSON, with the form of
            {
                "latitude" : float,
                "longitude" : float,
                "emergent_description" : String
            }

        :param image_file_path: The ODLC target image file name.
        :type image_file_path:  String

        :return: ID of the posted target.
        """
        odlc_target = Odlc(
            type="emergent",
            autonomous=False,
            latitude=target["latitude"],
            longitude=target["longitude"],
            description='Flint Hill School -- ODLC Emergent Target Submission: ' + str(target["emergent_description"]))

        # TODO: remove after testing
        """
        returned_odlc = self.client.post_odlc(odlc_target)

        with open(image_file_path) as img_file:
            self.client.post_odlc_image(returned_odlc.id, img_file.read())
        """
        missing_data = True

        while missing_data:
            try:
                returned_odlc = self.client.post_odlc(odlc_target)
                missing_data = False
            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE)

                try:
                    self.client = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                except:
                    print("Failed to connect to Interop., retrying...")

        missing_data = True

        with open(image_file_path) as img_file:
            while missing_data:
                try:
                    self.client.post_odlc_image(returned_odlc.id, img_file.read())
                    missing_data = False
                except:
                    sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE)

                    try:
                        self.client = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                    except:
                        print("Failed to connect to Interop., retrying...")

    def post_autonomous_target(self, target, image_file_path, index):
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

        :param image_file_path: The ODLC target image file name
        :type image_file_path: String

        :return: ID of the posted target
        """
        odlc_target = Odlc(
            type="standard",
            autonomous=True,
            latitude=target["image_processing_results"][index]["latitude"],
            longitude=target["image_processing_results"][index]["longitude"],
            orientation=target["image_processing_results"][index]["target_orientation"],
            shape=target["image_processing_results"][index]["target_shape_type"],
            background_color=target["image_processing_results"][index]["target_shape_color"],
            alphanumeric=target["image_processing_results"][index]["target_letter"],
            alphanumeric_color=target["image_processing_results"][index]["target_letter_color"],
            description="Flint Hill School -- ODLC Standard Target Submission")

        returned_odlc = self.client.post_odlc(odlc_target)

        with open(image_file_path) as img_file:
            self.client.post_odlc_image(returned_odlc.id, img_file.read())

#from interop import

#from interop import Telemetry
#from interop import Odlc
#from auvsi_suas import client
#from auvsi_suas.client import Odlc
#from auvsi_suas import Telemetry
from auvsi_suas.client import client
#from auvsi_suas.client import types
#from auvsi_suas.client.client import AsyncClient
#from auvsi_suas.client.types import Telemetry
from auvsi_suas.proto import interop_api_pb2

from .settings import GCSSettings
from time import sleep
from time import time
from requests.exceptions import ConnectionError


class InteropClientConverter(object):

    """
    Contains methods related to sending and receiving various data from the interop server.
    Contains a method to post our telemetry location to the interop server, get obstacles
    and mission data from the interop server, and send ODLC data to the interop server.
    """

    def __init__(self):
        try:
            print("got into init")
            #establishes interop connect. Creating an interop client object automatically makes a call to connect to interop
            self.client1 = client.Client(url=GCSSettings.INTEROP_URL, username=GCSSettings.INTEROP_USERNAME, password=GCSSettings.INTEROP_PASSWORD)
    #    self.asyncClient = AsyncClient(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
        except Exception as e: print(e)

    def post_telemetry(self, location, heading):
        """
        Post the drone's telemetry information.

        :param location:    The location to post.
        :type location:     Location
        :param heading:     The UAV's heading.
        :type heading:      Float
        """


        print (location)
        print(heading)
        missing_data = True

        while missing_data:
            try:
                telem_upload_data = interop_api_pb2.Telemetry()
                print("after telem upload data initialization  interopclient")
                telem_upload_data.longitude = location.get_lon()
                print("after get lon  interopclient")
                telem_upload_data.altitude = (location.get_alt() + GCSSettings.MSL_ALT)
                print("after get alt interopclient")
                telem_upload_data.latitude = location.get_lat()
                print("after get lat interopclient")
                telem_upload_data.heading = heading

                missing_data = False
            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE)

        print("before post_telemery statement interopclient")
        self.client1.post_telemetry(telem_upload_data)
        #print("exited loop"#)
#        try:
#            print("Begin connected ")
#            t = types.Telemetry(latitude=50, longitude=-76, altitude_msl=100, uas_heading=90)
#            client = Client(url="http://10.10.130.2:8000", username="testuser", password="testpass")
            #client = Client(args.url, args.username, password)

#            print("Successfullly connected ")
#            client.post_telemetry(t)

#        except Exception as e: print(e)

    def get_obstacles(self):
        """
        Return the obstacles.

        :return: [StationaryObstacle], [MovingObstacle]
        """
        missing_data = True
        while missing_data:
            try:
                #stationary_obstacles = self.client1.get_obstacles()
                #print("from interop_client.py get Obstacle")
                #print(stationary_obstacles)
            #    print(stationary_obstacles[0])
        #        print( len ( stationary_obstacles) )
                missing_data = False

            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE) # todo: 0.5

                try:
                    self.client1 = client.Client(url="http://192.168.1.86:8000", username="testuser", password="testpass")
                except:
                    print("Failed to connect to Interop., retrying...")
        print("inside get_obstacles()")
        #print(stationary_obstacles)
#        print(len (stationary_obstacles ))
        return stationary_obstacles

    def get_active_mission(self):
        """
        Get the active mission and return it. If no missions are active,
        then this function will return None.

        :return:        Active Mission.
        :return type:   Mission / None
        """
        missing_data = True
        mission =""



        while missing_data:
            try:
                print('inside get_active_mission ')
                missiontemp = self.client1.get_mission(2)
                print(missiontemp)
#                for missiontemp in missions:
#                if missiontemp.active:
#                    mission = missiontemp
#                    print(mission)
            #    else
            #        print("no active mission")
                missing_data = False
                return missiontemp

            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE) # todo: 0.5

                try:
                    client1 = client.Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                except:
                    print("Failed to connect to Interop., retrying...")

                try:
    #                for mission in missions:
                    print("inside the mission for loop")
                    if mission.active:
                        print("mission data")
                        print(mission)
                        return mission

                except:
                    print("Failed to get missions")




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

        missing_data = True

        while missing_data:
            try:
                returned_odlc = client1.post_odlc(odlc_target)
                missing_data = False
            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE) # todo: 0.5

                try:
                    client1 = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                except:
                    print("Failed to connect to Interop, retrying...")

        with open(image_file_path) as img_file:
            client1.post_odlc_image(returned_odlc.id, img_file.read())

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
        returned_odlc = client1.post_odlc(odlc_target)

        with open(image_file_path) as img_file:
            client1.post_odlc_image(returned_odlc.id, img_file.read())
        """
        missing_data = True

        while missing_data:
            try:
                returned_odlc = client1.post_odlc(odlc_target)
                missing_data = False
            except ConnectionError:
                sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE)

                try:
                    client1 = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                except:
                    print("Failed to connect to Interop., retrying...")

        missing_data = True

        with open(image_file_path) as img_file:
            while missing_data:
                try:
                    client1.post_odlc_image(returned_odlc.id, img_file.read())
                    missing_data = False
                except:
                    sleep(GCSSettings.INTEROP_DISCONNECT_RETRY_RATE)

                    try:
                        client1 = Client(GCSSettings.INTEROP_URL, GCSSettings.INTEROP_USERNAME, GCSSettings.INTEROP_PASSWORD)
                    except:
                        print("Failed to connect to Interop., retrying...")

    def post_autonomous_target(self, target_info):
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

        image_file_path = target_info["target"][0]["current_crop_path"]
        odlc_target = Odlc(
            type="standard",
            autonomous=True,
            latitude=target_info["target"][0]["latitude"],
            longitude=target_info["target"][0]["longitude"],
            orientation=target_info["target"][0]["target_orientation"],
            shape=target_info["target"][0]["target_shape_type"],
            background_color=target_info["target"][0]["target_shape_color"],
            alphanumeric=target_info["target"][0]["target_letter"],
            alphanumeric_color=target_info["target"][0]["target_letter_color"],
            description="Flint Hill School -- ODLC Standard Target Submission")

        returned_odlc = client1.post_odlc(odlc_target)

        with open(image_file_path) as img_file:
            client1.post_odlc_image(returned_odlc.id, img_file.read())
"""my_client = InteropClientConverter()

while True:
    #print(my_client.get_obstacles())
    time.sleep(1)"""

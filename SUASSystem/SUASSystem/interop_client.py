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

        Returned in the format: Mission
        """
        missions = self.client.get_missions()

        for mission in missions:
            if mission.active:
                return mission

        return None

    def get_client(self):
        """
        Return's the client
        """
        return self.client

if __name__ == "__main__":
    test_client = InteropClientConverter(6, "http://10.10.130.10:80", "flint", "8182105855")

    while True:
        print(test_client.get_obstacles())
        #print(test_client.get_active_mission())
        print("Connected...")
        sleep(0.5)

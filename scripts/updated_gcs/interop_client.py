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

    def post_telemetry(self, telemetry):
        """
        Post the drone's telemetry information

        :param telemetry: The telemetry to post
        :type telemetry: CurrentCoordinates
        """
        telem_upload_data = Telemetry(telemetry.get_latitude(), telemetry.get_longitude(), telemetry.get_altitude() + self.msl_alt, telemetry.get_heading())

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

if __name__ == "__main__":
    test_client = InteropClientConverter(22, "http://10.10.130.101:8000", "Flint", "2429875295")

    while True:
        test_client.get_obstacles()
        test_client.get_active_mission()

        sleep(0.5)

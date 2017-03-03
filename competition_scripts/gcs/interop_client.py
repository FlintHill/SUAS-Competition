from interop import AsyncClient
from interop import Telemetry

class InteropClientConverter:

    def __init__(self, msl_alt, url, username, password):
        self.msl_alt = msl_alt
        self.url = url
        self.username = username
        self.password = password

        print("BEFORE CLIENT()")
        self.client = AsyncClient(url, username, password)
        print("AFTER CLIENT()")

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
        return client.get_obstacles()

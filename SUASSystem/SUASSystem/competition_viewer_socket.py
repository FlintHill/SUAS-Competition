from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

class CompetitionViewerSocket(WebSocket):

    def __init__(self, p1, p2, p3, vehicle_state_data, mission_data):
        """
        Initialize
        """
        super(SDAViewSocket, self).__init__(p1, p2, p3)

        self.vehicle_state_data = vehicle_state_data
        self.mission_data = mission_data

    def handleMessage(self):
        data = '{"obstacle_present":' + str(self.vehicle_state_data[0].get_obstacle_in_path()).lower() +  ', '
        data += '"0": ' + str(self.mission_data[0]) + ', '
        data += '"alt": ' + str(self.vehicle_state_data[0].get_alt())
        data += ', "dir": ' + str(self.vehicle_state_data[0].get_direction())
        data += ', "speed": ' + str(self.vehicle_state_data[0].get_groundspeed())
        data += ', "velocity": ' + str(self.vehicle_state_data[0].get_velocity())
        data += ', "lat": ' + str(self.vehicle_state_data[0].get_lat()) + ', "long": ' + str(self.vehicle_state_data[0].get_lon()) + "}"
        data = data.replace("\'", "\"")

        self.sendMessage(u'' + data)

    def handleConnected(self):
       print (self.address, 'connected')

    def handleClose(self):
       print (self.address, 'closed')

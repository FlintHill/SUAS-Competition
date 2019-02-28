import SimpleWebSocketServer
import SUASSystem



def run_competition_viewer_process(vehicle_state_data, mission_information_data):
    competition_viewer_server = SimpleWebSocketServer.SimpleWebSocketServer('', 8000,
        SUASSystem.CompetitionViewerSocket,
        vehicle_state_data,
        mission_information_data
    )
    competition_viewer_server.serveforever()

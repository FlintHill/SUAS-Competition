import SimpleWebSocketServer
import SUASSystem

def run_competition_viewer_process(vehicle_state_data, mission_information_data):
    competition_viewer_server = SimpleWebSocketServer.SimpleWebSocketServer('', 8000,
        SUASSystem.CompetitionViewerSocket,
        vehicle_state_data,
        mission_information_data
    )
    competition_viewer_server.serveforever()

if __name__ == '__main__':
    demo_vehicle_state_data = [SUASSystem.VehicleState(10, 10, 10, 250, 5, [2,2,2], False, 2)]
    demo_mission_information_data = [{'stationary_obstacles': [{'latitude': 38.8711157, 'cylinder_height': 850.0, 'cylinder_radius': 25.0, 'longitude': -77.3221448}], 'fly_zones': [{'altitude_msl_max': 850.0, 'boundary_pts': [{'latitude': 38.8700862, 'order': 1, 'longitude': -77.3225069}, {'latitude': 38.870579, 'order': 2, 'longitude': -77.3233008}, {'latitude': 38.8719573, 'order': 3, 'longitude': -77.3210049}, {'latitude': 38.8712389, 'order': 4, 'longitude': -77.3210049}], 'altitude_msl_min': 450.0}], 'off_axis_target_pos': {'latitude': 0.0, 'longitude': 0.0}, 'moving_obstacles': [{'latitude': 0.0, 'altitude_msl': 0.0, 'cylinder_radius': 1.0, 'longitude': 0.0}], 'mission_waypoints': [{'latitude': 38.8706793, 'altitude_msl': 600.0, 'order': 1, 'longitude': -77.3227322}, {'latitude': 38.8713559, 'altitude_msl': 700.0, 'order': 2, 'longitude': -77.321949}, {'latitude': 38.8704955, 'altitude_msl': 600.0, 'order': 3, 'longitude': -77.3223996}], 'emergent_last_known_pos': {'latitude': 0.0, 'longitude': 0.0}, 'search_grid_points': [{'latitude': 38.8700862, 'altitude_msl': 450.0, 'order': 1, 'longitude': -77.3225069}, {'latitude': 38.870579, 'altitude_msl': 450.0, 'order': 2, 'longitude': -77.3233008}, {'latitude': 38.8719573, 'altitude_msl': 450.0, 'order': 3, 'longitude': -77.3210049}, {'latitude': 38.8712389, 'altitude_msl': 450.0, 'order': 4, 'longitude': -77.3210049}], 'home_pos': {'latitude': 38.8711157, 'longitude': -77.3214769}, 'air_drop_pos': {'latitude': 38.8715584, 'longitude': -77.3214769}}]

    run_competition_viewer_process(demo_vehicle_state_data, demo_mission_information_data)

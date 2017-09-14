import SUASSystem
import multiprocessing
from SUASSystem.logging import log
from time import sleep

def run_sda_process(logger_queue, waypoints, sda_status, sda_avoid_coords, vehicle_state_data, mission_information_data):
    SUASSystem.logging.logger_worker_configurer(logger_queue)
    logger_name = multiprocessing.current_process().name

    log(logger_name, "Instantiating SDA converter")
    while True:
        try:
            sda_converter = SUASSystem.SDAConverter(vehicle_state_data[0].get_location(), mission_information_data[0]["fly_zones"])
            break
        except:
            sleep(0.1)
    log(logger_name, "SDA converter instantiated")

    while True:
        if "enabled" in str(sda_status.value).lower():
            current_location = vehicle_state_data[0].get_location()

            current_waypoint_number = vehicle_state_data[0].get_current_waypoint_number()
            if current_waypoint_number != 0:
                current_uav_waypoint = waypoints[current_waypoint_number - 1]
                sda_converter.set_waypoint(SUASSystem.Location(current_uav_waypoint.x, current_uav_waypoint.y, current_uav_waypoint.z * 3.28084))
            else:
                sda_converter.set_waypoint(SUASSystem.Location(waypoints[1].x, waypoints[1].y, waypoints[1].z))

            sda_converter.reset_obstacles()
            for stationary_obstacle in mission_information_data["stationary_obstacles"]:
                sda_converter.add_obstacle(get_obstacle_location(stationary_obstacle, MSL_ALT), stationary_obstacle)
            for moving_obstacle in mission_information_data["moving_obstacles"]:
                sda_converter.add_obstacle(get_obstacle_location(moving_obstacle, MSL_ALT), moving_obstacle)

            sda_converter.set_uav_position(current_location)
            sda_converter.avoid_obstacles()

            if not sda_converter.has_uav_completed_guided_path():
                try:
                    sda_avoid_coords[0] = sda_converter.get_uav_avoid_coordinates()
                except:
                    sda_avoid_coords.append(sda_converter.get_uav_avoid_coordinates())

        sleep(0.5)

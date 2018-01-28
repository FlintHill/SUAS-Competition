import SUASSystem
import multiprocessing
from SUASSystem.suas_logging import log
from time import sleep
import traceback
import numpy

def run_sda_process(logger_queue, waypoints, sda_status, sda_avoid_coords, UAV_status, vehicle_state_data, mission_information_data):
    SUASSystem.suas_logging.logger_worker_configurer(logger_queue)
    logger_name = multiprocessing.current_process().name
    log(logger_name, "Instantiating SDA converter")
    while True:
        try:
            sda_converter = SUASSystem.SDAConverter(vehicle_state_data[0].get_location(), mission_information_data[0]["fly_zones"])
            break
        except:
            sleep(0.1)
    log(logger_name, "SDA converter instantiated")
    starting_coords = vehicle_state_data[0].get_location()

    while True:
        if sda_status.value == "connected":#if True:
            current_location = vehicle_state_data[0].get_location()
            current_location.alt = current_location.get_alt() - SUASSystem.GCSSettings.MSL_ALT
            current_waypoint_number = vehicle_state_data[0].get_current_waypoint_number()
            print("Pre add obstacles", mission_information_data[0]["stationary_obstacles"])
            if current_waypoint_number != 0:
                current_uav_waypoint = waypoints[current_waypoint_number - 1]
                current_uav_waypoint_location = SUASSystem.Location(current_uav_waypoint.x, current_uav_waypoint.y, current_uav_waypoint.z * 3.28084)
                print('WAYPOINT INFO')
                print(current_waypoint_number-1)
                print('command number')
                print(int(current_uav_waypoint.command))
                if is_waypoint_avoidable(current_uav_waypoint) and not is_uav_at_location(current_location, current_uav_waypoint_location):
                    sda_converter.set_waypoint(current_uav_waypoint_location)

                    sda_converter.reset_obstacles()
                    for stationary_obstacle in mission_information_data[0]["stationary_obstacles"]:
                        sda_converter.add_obstacle(stationary_obstacle)
                    sda_converter.set_uav_position(current_location)
                    if not UAV_status.value == "GUIDED":
                        sda_converter.avoid_obstacles()
                    print('The current xy coordinates of the UAV:')
                    print(SUASSystem.convert_to_point(starting_coords, current_location))
                    print('The current sda avoid coordinates for the UAV in regards to the obstacle:')
                    print(sda_avoid_coords)

                    if not sda_converter.has_uav_completed_guided_path():
                        UAV_status.value = "GUIDED"
                        try:
                            sda_avoid_coords[0] = sda_converter.get_uav_avoid_coordinates()
                        except:
                            sda_avoid_coords.append(sda_converter.get_uav_avoid_coordinates())

                    if sda_converter.has_uav_completed_guided_path():
                        UAV_status.value = "AUTO"
                        sda_converter.current_path = numpy.array([])

        sleep(0.5)

def is_waypoint_avoidable(uav_waypoint):
    non_avoidable_waypoint_command_types = [22, 183, 20]

    for non_avoidable_waypoint_command_type in non_avoidable_waypoint_command_types:
        if int(uav_waypoint.command) == non_avoidable_waypoint_command_type:
            print('Waypoint is not avoidable')
            return False

    return True

def is_uav_at_location(current_location, waypoint_location, threshold_dist=5):
    dx, dy, dz = SUASSystem.haversine(waypoint_location, current_location)
    euclidean_dist = (dx**2 + dy**2 + dz**2)**0.5

    if euclidean_dist < threshold_dist:
        return True

    return False

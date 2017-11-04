import SUASSystem
import multiprocessing
from SUASSystem.suas_logging import log
from time import sleep
import traceback

def run_sda_process(logger_queue, waypoints, sda_status, sda_avoid_coords, UAV_status, vehicle_state_data, mission_information_data):
    SUASSystem.suas_logging.logger_worker_configurer(logger_queue)
    logger_name = multiprocessing.current_process().name
    boundary_points = [
            {
                "boundary_pts" : [
                    {"latitude" : 38.1424887, "longitude" : -76.4344168, "order" : 0},
                    {"latitude" : 38.1430962, "longitude" : -76.4248037, "order" : 1},
                    {"latitude" : 38.1517193, "longitude" : -76.4261985, "order" : 2},
                    {"latitude" : 38.1513987, "longitude" : -76.4351463, "order" : 3}
                ]
            }
        ]
    log(logger_name, "Instantiating SDA converter")
    while True:
        try:
            sda_converter = SUASSystem.SDAConverter(vehicle_state_data[0].get_location(), boundary_points)
            break
        except:
            sleep(0.1)
    log(logger_name, "SDA converter instantiated")

    while True:
        if True:#sda_status.value == "connected":
            try:
                current_location = vehicle_state_data[0].get_location()
                current_location.alt = current_location.get_alt() - SUASSystem.GCSSettings.MSL_ALT
                current_waypoint_number = vehicle_state_data[0].get_current_waypoint_number()
                print("Current waypoint number: " + str(current_waypoint_number))
                if current_waypoint_number != 0:
                    current_uav_waypoint = waypoints[current_waypoint_number - 1]
                    sda_converter.set_waypoint(SUASSystem.Location(current_uav_waypoint.x, current_uav_waypoint.y, current_uav_waypoint.z * 3.28084))

                    """sda_converter.reset_obstacles()
                    #for stationary_obstacle in mission_information_data["stationary_obstacles"]:
                    #    sda_converter.add_obstacle(get_obstacle_location(stationary_obstacle, MSL_ALT), stationary_obstacle)
                    #for moving_obstacle in mission_information_data["moving_obstacles"]:
                    #    sda_converter.add_obstacle(get_obstacle_location(moving_obstacle, MSL_ALT), moving_obstacle)"""
                    sda_converter.set_uav_position(current_location)
                    #if len(sda_avoid_coords) == 0:
                    #    sda_converter.avoid_obstacles()
                    sda_converter.avoid_obstacles()
                    print("has completed guided path before")
                    print(sda_converter.has_uav_completed_guided_path())
                    print('length of sda avoid coords')
                    print(len(sda_avoid_coords))
                    print('current sda avoid coords')
                    print(sda_avoid_coords)
                    if not sda_converter.has_uav_completed_guided_path(): #and len(sda_avoid_coords) == 0:
                        UAV_status.value = "GUIDED"
                        try:
                            print('sets new sda avoid coords')
                            sda_avoid_coords[0] = sda_converter.get_uav_avoid_coordinates()
                            print('new sda avoid coords')
                            print(sda_avoid_coords)
                        except:
                            print('in the except block')
                            print('has it completed guided path', str(sda_converter.has_uav_completed_guided_path()))
                            print('sets new sda avoid coords')
                            sda_avoid_coords.append(sda_converter.get_uav_avoid_coordinates())
                            print('new sda avoid coords')
                            print(sda_avoid_coords)

                    if sda_converter.has_uav_completed_guided_path():
                        UAV_status.value = "AUTO"
            except:
                traceback.print_exc()
                print('IN EXCEPT BLOCK')

        sleep(0.5)

import multiprocessing
import SUASSystem
import dronekit
import time
import numpy
from .suas_logging import *
from .settings import GCSSettings
from time import sleep
from .converter_functions import *

gcs_logger_name = multiprocessing.current_process().name

def gcs_process(sda_status, img_proc_status, interop_client_array, targets_to_submit):
    # Setup logging information
    logger_queue = multiprocessing.Queue(-1)
    logger_listener_process = multiprocessing.Process(target=listener_process, args=(
        logger_queue,
        logger_listener_configurer
    ))
    logger_listener_process.start()
    logger_worker_configurer(logger_queue)

    manager = multiprocessing.Manager()
    vehicle_state_data = manager.list()
    mission_information_data = manager.list()
    sda_avoid_coords = manager.list()
    UAV_status = manager.Value('s', "AUTO")
    location_log = manager.list()
    vehicle = connect_to_vehicle()
    waypoints = download_waypoints(vehicle)

    if len(interop_client_array) != 0:
        mission_information_data.append(get_mission_json(interop_client_array[0].get_active_mission(), interop_client_array[0].get_obstacles()))
    else:
        print("[Error] : The GCS process is unable to load mission data from the Interoperability server")
        mission_information_data.append({})
    vehicle_state_data.append(SUASSystem.get_vehicle_state(vehicle, GCSSettings.MSL_ALT))

    competition_viewer_process = initialize_competition_viewer_process(vehicle_state_data, mission_information_data)
    img_proc_process = initialize_image_processing_process(logger_queue, location_log, targets_to_submit, interop_client_array)
    autonomous_img_proc_process = initialize_autonomous_image_processing_process(logger_queue, location_log, [], interop_client_array, img_proc_status)
    sda_process = initialize_sda_process(logger_queue, sda_status, UAV_status, waypoints, sda_avoid_coords, vehicle_state_data, mission_information_data)
    log(gcs_logger_name, "Completed instantiation of all child processes")

    while True:
        current_location = get_location(vehicle)
        current_location_json = {
            "current_location": current_location,
            "epoch_time": time.time()
        }
        location_log.append(current_location_json)

        vehicle_state_data[0] = SUASSystem.get_vehicle_state(vehicle, GCSSettings.MSL_ALT)

        if len(interop_client_array) != 0:
            interop_client_array[0].post_telemetry(current_location, vehicle_state_data[0].get_direction())
            mission_information_data[0] = get_mission_json(interop_client_array[0].get_active_mission(), interop_client_array[0].get_obstacles())

        if (vehicle.location.global_relative_frame.alt * 3.28084) > GCSSettings.SDA_MIN_ALT and sda_status.value.lower() == "connected":
            if (UAV_status.value == "GUIDED"):
                sda_avoid_feet_height = Location(sda_avoid_coords[0].get_lat(), sda_avoid_coords[0].get_lon(), sda_avoid_coords[0].get_alt()*3.28084)
                log("root", "Avoiding obstacles...")
                vehicle.mode = dronekit.VehicleMode("GUIDED")
                vehicle.simple_goto(sda_avoid_coords[0].as_global_relative_frame())
            if UAV_status.value == 'AUTO' and vehicle.mode.name != "AUTO":
                vehicle.mode = dronekit.VehicleMode("AUTO")


        sleep(0.25)

def initialize_competition_viewer_process(vehicle_state_data, mission_information_data):
    log(gcs_logger_name, "Instantiating Competition Viewer process")
    competition_viewer_process = multiprocessing.Process(target=SUASSystem.run_competition_viewer_process, args=(
        vehicle_state_data,
        mission_information_data,
    ))
    competition_viewer_process.start()
    log(gcs_logger_name, "Competition Viewer process instantiated")

    return competition_viewer_process

def initialize_sda_process(logger_queue, sda_status, UAV_status, waypoints, sda_avoid_coords, vehicle_state_data, mission_information_data):
    log(gcs_logger_name, "Instantiating SDA process")
    sda_process = multiprocessing.Process(target=SUASSystem.run_sda_process, args=(
        logger_queue,
        waypoints,
        sda_status,
        sda_avoid_coords,
        UAV_status,
        vehicle_state_data,
        mission_information_data,
    ))
    sda_process.start()
    log(gcs_logger_name, "SDA process instantiated")

    return sda_process

def initialize_image_processing_process(logger_queue, location_log, targets_to_submit, interop_client_array):
    log(gcs_logger_name, "Instantiating Image Processing process")
    img_proc_process = multiprocessing.Process(target=SUASSystem.run_img_proc_process, args=(
        logger_queue,
        location_log,
        targets_to_submit,
        interop_client_array
    ))
    img_proc_process.start()
    log(gcs_logger_name, "Image Processing process instantiated")

    return img_proc_process

def initialize_autonomous_image_processing_process(logger_queue, location_log, interop_client_array, img_proc_status):
    log(gcs_logger_name, "Instantiating Autonomous Image Processing process")
    auto_img_proc_process = multiprocessing.Process(target=SUASSystem.run_autonomous_img_proc_process, args=(
        logger_queue,
        location_log,
        targets_to_submit,
        interop_client_array,
        img_proc_status,
    ))
    auto_img_proc_process.start()
    log(gcs_logger_name, "Autonomous Image Processing process instantiated")

    return auto_img_proc_process

def connect_to_vehicle():
    log(gcs_logger_name, "Connecting to UAV on: %s" % GCSSettings.UAV_CONNECTION_STRING)
    vehicle = dronekit.connect(GCSSettings.UAV_CONNECTION_STRING, wait_ready=True)
    vehicle.wait_ready('autopilot_version')
    log(gcs_logger_name, "Connected to UAV on: %s" % GCSSettings.UAV_CONNECTION_STRING)
    SUASSystem.suas_logging.log_vehicle_state(vehicle, gcs_logger_name)

    return vehicle

def download_waypoints(vehicle):
    log(gcs_logger_name, "Downloading waypoints from UAV on: %s" % GCSSettings.UAV_CONNECTION_STRING)
    waypoints = vehicle.commands
    waypoints.download()
    waypoints.wait_ready()
    log(gcs_logger_name, "Waypoints successfully downloaded from UAV on: %s" % GCSSettings.UAV_CONNECTION_STRING)

    return waypoints

def has_uav_reached_waypoint(current_location, waypoint_location, threshold_dist=2):
    dx, dy, dz = SUASSystem.haversine(waypoint_location, current_location)
    euclidean_dist = (dx**2 + dy**2 + dz**2)**0.5

    if euclidean_dist < threshold_dist:
        return True

    return False

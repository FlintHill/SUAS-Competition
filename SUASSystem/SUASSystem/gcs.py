import multiprocessing
import SUASSystem
import dronekit
from SUASSystem.logging import log
from SUASSystem import GCSSettings
from time import sleep

# Setup logging information
logger_queue = multiprocessing.Queue(-1)
logger_listener_process = multiprocessing.Process(target=SUASSystem.logging.listener_process, args=(
    logger_queue,
    SUASSystem.logging.logger_listener_configurer
))
logger_listener_process.start()
SUASSystem.logging.logger_worker_configurer(logger_queue)
gcs_logger_name = multiprocessing.current_process().name

def gcs_process(sda_status, img_proc_status, interop_position_update_rate):
    manager = multiprocessing.Manager()
    vehicle_state_data = manager.list()
    mission_information_data = manager.list()
    targets_to_submit = manager.list()
    sda_avoid_coords = manager.list()
    location_log = manager.list()

    vehicle = connect_to_vehicle()
    waypoints = download_waypoints(vehicle)

    competition_viewer_process = initialize_competition_viewer_process(vehicle_state_data, mission_information_data)
    img_proc_process = initialize_image_processing_process(img_proc_status, location_log, targets_to_submit)
    sda_process = initialize_sda_process(sda_status, waypoints, sda_avoid_coords, vehicle_state_data, mission_information_data)
    log(gcs_logger_name, "Completed instantiation of all child processes")

    guided_waypoint_location = None
    vehicle_state_data.append(SUASSystem.get_vehicle_state(vehicle, GCSSettings.MSL_ALT))
    while True:
        interop_position_update_rate.value += 1
        vehicle_state_data[0] = SUASSystem.get_vehicle_state(vehicle, GCSSettings.MSL_ALT)

        print("LIVE")
        print(current_location)
        current_location = SUASSystem.Location(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt)
        location_log.append(current_location)
        """if (vehicle.location.global_relative_frame.alt * 3.28084) > GCSSettings.SDA_MIN_ALT and (vehicle.mode.name == "GUIDED" or vehicle.mode.name == "AUTO"):
            log("root", "Avoiding obstacles...")
            vehicle.mode = VehicleMode("GUIDED")
            guided_waypoint_location = sda_avoid_coords[0][0]
            vehicle.simple_goto(guided_waypoint_location.as_global_relative_frame())

        if waypoint_location:
            if vehicle.mode.name == "GUIDED" and has_uav_reached_waypoint(current_location, guided_waypoint_location):
                vehicle.mode = VehicleMode("AUTO")"""

        sleep(0.1)

def initialize_competition_viewer_process(vehicle_state_data, mission_information_data):
    log(gcs_logger_name, "Instantiating Competition Viewer process")
    competition_viewer_process = multiprocessing.Process(target=SUASSystem.run_competition_viewer_process, args=(
        vehicle_state_data,
        mission_information_data,
    ))
    competition_viewer_process.start()
    log(gcs_logger_name, "Competition Viewer process instantiated")

    return competition_viewer_process

def initialize_sda_process(sda_status, waypoints, sda_avoid_coords, vehicle_state_data, mission_information_data):
    log(gcs_logger_name, "Instantiating SDA process")
    sda_process = multiprocessing.Process(target=SUASSystem.run_sda_process, args=(
        logger_queue,
        waypoints,
        sda_status,
        sda_avoid_coords,
        vehicle_state_data,
        mission_information_data,
    ))
    #sda_process.start()
    log(gcs_logger_name, "SDA process instantiated")

    return sda_process

def initialize_image_processing_process(img_proc_status, location_log, targets_to_submit):
    log(gcs_logger_name, "Instantiating Image Processing process")
    img_proc_process = multiprocessing.Process(target=SUASSystem.run_img_proc_process, args=(
        logger_queue,
        img_proc_status,
        location_log,
        targets_to_submit
    ))
    #img_proc_process.start()
    log(gcs_logger_name, "Image Processing process instantiated")

    return img_proc_process

def connect_to_vehicle():
    log(gcs_logger_name, "Connecting to UAV on: %s" % GCSSettings.UAV_CONNECTION_STRING)
    vehicle = dronekit.connect(GCSSettings.UAV_CONNECTION_STRING, wait_ready=True)
    vehicle.wait_ready('autopilot_version')
    log(gcs_logger_name, "Connected to UAV on: %s" % GCSSettings.UAV_CONNECTION_STRING)
    SUASSystem.logging.log_vehicle_state(vehicle, gcs_logger_name)

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

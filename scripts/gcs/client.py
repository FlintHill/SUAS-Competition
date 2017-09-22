from dronekit import connect, VehicleMode
import socket
import multiprocessing
from datetime import datetime
from SUASSystem.logging import *
from time import sleep
from SUASSystem import *
from SimpleWebSocketServer import SimpleWebSocketServer
from SDA import *
from ImgProcessingCLI.Runtime.RuntimeTarget import RuntimeTarget
from ImgProcessingCLI.DataMine.OrientationSolver import OrientationSolver
from ImgProcessingCLI.DataMine import KMeansCompare
from ImgProcessingCLI.Runtime import TargetCropper3
from EigenFit.DataMine import Categorizer
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
from ImgProcessingCLI.Runtime.GeoStamps import GeoStamps
from EigenFit.Load import *
from ImgProcessingCLI.Runtime.TargetCrop import TargetCrop
from timeit import default_timer
import rawpy
import shutil
import PIL
import exifread

UAV_CONNECTION_STRING = "tcp:127.0.0.1:14551"

INTEROP_URL = "http://10.10.130.2:8000"
INTEROP_USERNAME = "Flint"
INTEROP_PASSWORD = "271824758"

MSL_ALT = 446.42
SDA_MIN_ALT = 110

GENERATED_DATA_LOCATION = "image_data"
'''
BASE_LETTER_CATEGORIZER_PCA_PATH
Vale's path: /Users/vtolpegin/Desktop/GENERATED FORCED WINDOW PCA
Peter's Path: /Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED FORCED WINDOW PCA
'''
VALE_BASE_LETTER_CATEGORIZER_PATH = "/Users/vtolpegin/Desktop/GENERATED FORCED WINDOW PCA"
PETER_BASE_LETTER_CATEGORIZER_PATH = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED FORCED WINDOW PCA"
BASE_LETTER_CATEGORIZER_PCA_PATH = PETER_BASE_LETTER_CATEGORIZER_PATH
'''
BASE_ORIENTATION_CLASSIFIER_PCA_PATH:
Vale's path: /Users/vtolpegin/Desktop/GENERATED 180 ORIENTATION PCA
Peter's path: /Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED 180 ORIENTATION PCA
'''
VALE_BASE_ORIENTATION_CLASSIFIER_PCA_PATH = "/Users/vtolpegin/Desktop/GENERATED 180 ORIENTATION PCA"
PETER_BASE_ORIENTATION_CLASSIFIER_PCA_PATH = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED 180 ORIENTATION PCA"
BASE_ORIENTATION_CLASSIFIER_PCA_PATH = PETER_BASE_ORIENTATION_CLASSIFIER_PCA_PATH

SD_CARD_NAME = "NX500"

MIN_DIST_BETWEEN_TARGETS_KM = 30.0/1000.0

def sda_viewer_process(logger_queue, configurer, vehicle_state_data, mission_data):
    """
    Creates a process for the SDA viewer

    :param vehicle_state_process: The vehicle's current state
    :type vehicle_state_process: multiprocessing.Array
    """
    configurer(logger_queue)
    name = multiprocessing.current_process().name

    log(name, "Instantiating SDA Viewer process")
    sda_viewer_server = SimpleWebSocketServer('', 8000, SDAViewSocket, vehicle_state_data, mission_data)
    sda_viewer_server.serveforever()
    log(name, "SDA Viewer process instantiated")

def get_image_timestamp(filename):
    """
    Returns an image's timestamp
    """
    opened_file = open(filename, 'rb')
    tags = exifread.process_file(opened_file)
    image_raw_time = tags['Image DateTime']
    converted_time = datetime.strptime(str(image_raw_time), "%Y:%m:%d %H:%M:%S")

    return converted_time

def target_listener(logger_queue, configurer, timestamped_location_data_array):
    """
    Run targets and submit them to the interoperability server
    """
    configurer(logger_queue)
    name = multiprocessing.current_process().name

    #interop_server_client = InteropClientConverter(MSL_ALT, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

    log(name, "Instantiating letter categorizer")
    eigenvectors = load_numpy_arr(BASE_LETTER_CATEGORIZER_PCA_PATH + "/Data/Eigenvectors/eigenvectors 0.npy")
    projections_path = BASE_LETTER_CATEGORIZER_PCA_PATH + "/Data/Projections"
    mean = load_numpy_arr(BASE_LETTER_CATEGORIZER_PCA_PATH + "/Data/Mean/mean_img 0.npy")
    num_dim = 20
    letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, num_dim)
    log(name, "Letter categorizer instantiated successfully")

    log(name, "Instantiating orientation solver")
    orientation_eigenvectors = load_numpy_arr(BASE_ORIENTATION_CLASSIFIER_PCA_PATH + "/Data/Eigenvectors/eigenvectors 0.npy")
    orientation_projections_path = BASE_ORIENTATION_CLASSIFIER_PCA_PATH + "/Data/Projections"
    orientation_mean = load_numpy_arr(BASE_ORIENTATION_CLASSIFIER_PCA_PATH + "/Data/Mean/mean_img 0.npy")
    orientation_num_dim = 50
    orientation_solver = OrientationSolver(orientation_eigenvectors, orientation_mean, BASE_ORIENTATION_CLASSIFIER_PCA_PATH, orientation_num_dim)
    log(name, "Orientation solver instantiated")

    if os.path.exists(GENERATED_DATA_LOCATION):
        shutil.rmtree(GENERATED_DATA_LOCATION)

    os.mkdir(GENERATED_DATA_LOCATION)
    os.mkdir(os.path.join(GENERATED_DATA_LOCATION, "object_file_format"))

    sd_path = os.path.join("/Volumes", SD_CARD_NAME, "DCIM")
    gps_coords = []
    gps_update_index = 0
    while True:
        if len(timestamped_location_data_array) != 0:
            if timestamped_location_data_array[0]["index"] != gps_update_index:
                gps_coords.append(timestamped_location_data_array[0]["geo_stamp"])
                gps_update_index += 1

        print("Waiting for path to exist...")

        # Wait for SD card to be loaded
        if True:#os.path.exists(sd_path):
            break

        sleep(1)

    # Once SD card is loaded, begin processing
    # For every image on the SD card
    # 1. Load the image
    # 2. Process the crops, determine the ones that are targets
    # 3. Save the targets to GENERATED_DATA_LOCATION
    # 4. Upload the targets to interop server
    log(name, "Beginning image processing...")
    geo_stamps = GeoStamps([GeoStamp([38.38875, -77.27532], datetime.now())])#gps_coords)
    crop_index = 0

    all_target_crops = []
    for pic_folder in os.listdir(sd_path):
        pictures_dir_path = os.path.join(sd_path, pic_folder)

        for pic_name in os.listdir(pictures_dir_path):
            if ".SRW" in pic_name:
                start_time = default_timer()
                log(name, "Loading image " + pic_name)
                pic_path = os.path.join(pictures_dir_path, pic_name)
                img = rawpy.imread(pic_path).postprocess()
                rgb_image = Image.fromarray(numpy.roll(img, 1, axis=0))
                image_timestamp = get_image_timestamp(pic_path)

                target_crops = TargetCropper3.get_target_crops_from_img(rgb_image, image_timestamp, geo_stamps, 6)
                target_crops = TargetCrop.get_non_duplicate_crops(all_target_crops, target_crops, MIN_DIST_BETWEEN_TARGETS_KM)
                all_target_crops.extend(target_crops)
                log(name, "Finished processing " + pic_name + " in " + str(default_timer() - start_time) + " seconds")

                for target_crop in target_crops:
                    try:
                        log(name, "Identifying target characteristics of target #" + str(crop_index))
                        runtime_target = RuntimeTarget(target_crop, letter_categorizer, orientation_solver)
                        target_json_output = runtime_target.get_competition_json_output()

                        log(name, "Saving target characteristics of target #" + str(crop_index))
                        output_pic_name = os.path.join(GENERATED_DATA_LOCATION, "object_file_format", str(crop_index) + ".png")
                        output_json_name = os.path.join(GENERATED_DATA_LOCATION, "object_file_format", str(crop_index) + ".txt")
                        save_json_data(output_json_name, {"target_json_output" : "Testing"})#target_json_output)
                        target_crop.get_crop_img().save(output_pic_name)

                        crop_index += 1
                    except:
                        log(name, "ERROR: Could not process a target crop")

    if crop_index != 0:
        interop_client = interop_server_client.get_client()

        upload_targets(interop_client, os.path.join(GENERATED_DATA_LOCATION, "object_file_format"), team_id=INTEROP_USERNAME)

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    interop_server_client = InteropClientConverter(MSL_ALT, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

    logger_queue = multiprocessing.Queue(-1)
    logger_listener_process = multiprocessing.Process(target=listener_process, args=(logger_queue, logger_listener_configurer))
    logger_listener_process.start()

    timestamped_location_data_array = manager.list()
    target_listener_process = multiprocessing.Process(target=target_listener, args=(logger_queue, logger_worker_configurer, timestamped_location_data_array))
    #target_listener_process.start()
    target_listener(logger_queue, logger_worker_configurer, timestamped_location_data_array)
    while True:
        sleep(0.5)

    vehicle_state_data = manager.list()
    mission_data = manager.list()
    sda_viewer_process = multiprocessing.Process(target=sda_viewer_process, args=(logger_queue, logger_worker_configurer, vehicle_state_data, mission_data))
    sda_viewer_process.start()

    logger_worker_configurer(logger_queue)
    name = multiprocessing.current_process().name

    log(name, "Connecting to UAV on: %s" % UAV_CONNECTION_STRING)
    vehicle = connect(UAV_CONNECTION_STRING, wait_ready=True)
    vehicle.wait_ready('autopilot_version')
    log(name, "Connected to UAV on: %s" % UAV_CONNECTION_STRING)
    log_vehicle_state(vehicle, name)

    log(name, "Waiting for UAV to be armable")
    log(name, "Waiting for UAV to load waypoints")

    log(name, "Downloading waypoints from UAV on: %s" % UAV_CONNECTION_STRING)
    waypoints = vehicle.commands
    waypoints.download()
    waypoints.wait_ready()
    log(name, "Waypoints successfully downloaded")

    #gps_update_index = 0
    current_location = get_location(vehicle)
    """timestamped_location_data_array.append({
        "index" : gps_update_index,
        "geo_stamp" : GeoStamp((current_location.get_lat(), current_location.get_lon()), datetime.now().strftime("%h %M %S"))
    })"""
    stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
    obstacles_array = [stationary_obstacles, moving_obstacles]
    mission_data.append(get_mission_json(interop_server_client.get_active_mission(), obstacles_array))

    """log(name, "Enabling SDA...")
    sda_converter = SDAConverter(get_location(vehicle), mission_data[0]["fly_zones"])
    sda_converter.set_waypoint(Location(waypoints[1].x, waypoints[1].y, waypoints[1].z))
    log(name, "SDA enabled")"""

    vehicle_state_data.append(get_vehicle_state(vehicle, None, MSL_ALT))#sda_converter, MSL_ALT))

    log(name, "Everything is instantiated...Beginning operation")
    while True:
        current_location = get_location(vehicle)
        """current_waypoint_number = vehicle.commands.next
        if current_waypoint_number != 0:
            current_uav_waypoint = waypoints[current_waypoint_number - 1]
            sda_converter.set_waypoint(Location(current_uav_waypoint.x, current_uav_waypoint.y, current_uav_waypoint.z * 3.28084))"""

        interop_server_client.post_telemetry(current_location, vehicle.heading)
        """gps_update_index += 1
        timestamped_location_data_array[0] = {
            "index" : gps_update_index,
            "geo_stamp" : GeoStamp((current_location.get_lat(), current_location.get_lon()), datetime.now())
        }"""
        stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
        obstacles_array = [stationary_obstacles, moving_obstacles]
        """sda_converter.reset_obstacles()
        for stationary_obstacle in stationary_obstacles:
            sda_converter.add_obstacle(get_obstacle_location(stationary_obstacle, MSL_ALT), stationary_obstacle)
        for moving_obstacle in moving_obstacles:
            sda_converter.add_obstacle(get_obstacle_location(moving_obstacle, MSL_ALT), moving_obstacle)"""

        vehicle_state_data[0] = get_vehicle_state(vehicle, None, MSL_ALT)#)#sda_converter, MSL_ALT)
        mission_data[0] = get_mission_json(interop_server_client.get_active_mission(), obstacles_array)

        #sda_converter.set_uav_position(current_location)
        #sda_converter.avoid_obstacles()

        """if (vehicle.location.global_relative_frame.alt * 3.28084) > SDA_MIN_ALT and (vehicle.mode.name == "GUIDED" or vehicle.mode.name == "AUTO"):
            if not sda_converter.has_uav_completed_guided_path():
                log("root", "Avoiding obstacles...")
                print(sda_converter.get_uav_avoid_coordinates())
                vehicle.mode = VehicleMode("GUIDED")
                vehicle.simple_goto(sda_converter.get_uav_avoid_coordinates())

        if vehicle.mode.name == "GUIDED" and sda_converter.has_uav_completed_guided_path() and sda_converter.does_guided_path_exist():
            vehicle.mode = VehicleMode("AUTO")"""

        sleep(0.1)

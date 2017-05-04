from dronekit import connect, VehicleMode
import socket
import multiprocessing
from datetime import datetime
from logger import *
from time import sleep
from interop_client import InteropClientConverter
from sda_converter import SDAConverter
from converter_functions import *
from sda_viewer import SDAViewSocket
from SimpleWebSocketServer import SimpleWebSocketServer
from vehicle_state import VehicleState
from SDA import *
from ImgProcessingCLI.Runtime.RuntimeTarget import RuntimeTarget
from ImgProcessingCLI.DataMine.OrientationSolver import OrientationSolver
from ImgProcessingCLI.DataMine import KMeansCompare
from ImgProcessingCLI.Runtime import TargetCropper
from EigenFit.DataMine import Categorizer
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
from ImgProcessingCLI.Runtime.GeoStamps import GeoStamps
from EigenFit.Load import *
from timeit import default_timer
import rawpy
import cv2
import shutil
import PIL

TK1_ADDRESS = ('192.168.1.6', 9001)

UAV_CONNECTION_STRING = "tcp:127.0.0.1:14551"

INTEROP_URL = "http://10.10.130.2:8000"
INTEROP_USERNAME = "Flint"
INTEROP_PASSWORD = "2429875295"

MSL_ALT = 430
MIN_REL_FLYING_ALT = 100
MAX_REL_FLYING_ALT = 750

GENERATED_DATA_LOCATION = "image_data"
BASE_LETTER_CATEGORIZER_PCA_PATH = "/Users/vtolpegin/Desktop/GENERATED FORCED WINDOW PCA"
BASE_ORIENTATION_CLASSIFIER_PCA_PATH = "/Users/vtolpegin/Desktop/GENERATED 180 ORIENTATION PCA"

SD_CARD_NAME = "NX500"

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

    if not os.path.exists(GENERATED_DATA_LOCATION):
        os.mkdir(GENERATED_DATA_LOCATION)
    else:
        shutil.rmtree(GENERATED_DATA_LOCATION)
        os.mkdir(GENERATED_DATA_LOCATION)

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
        if os.path.exists(sd_path):
            break

        sleep(1)

    # Once SD card is loaded, begin processing
    # For every image on the SD card
    # 1. Load the image
    # 2. Process the crops, determine the ones that are targets
    # 3. Save the targets to GENERATED_DATA_LOCATION
    # 4. Upload the targets to interop server
    log(name, "Beginning image processing...")
    for pic_folder in os.listdir(sd_path):
        pictures_dir_path = os.path.join(sd_path, pic_folder)

        for pic_name in os.listdir(pictures_dir_path):
            if ".SRW" in pic_name:
                start_time = default_timer()
                log(name, "Loading image " + pic_name)
                pic_path = os.path.join(pictures_dir_path, pic_name)
                img = rawpy.imread(pic_path).postprocess()
                rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                rgb_image = Image.fromarray(rgb_image).convert('RGB')

                print("BEFORE TargetCropper")
                target_crops = TargetCropper.get_target_crops_from_img2(rgb_image, GeoStamps(gps_coords), 6)
                print("AFTER TargetCropper")
                #print(len(target_crops))

                log(name, "Finished processing " + pic_name)
                print(default_timer() - start_time)
                exit()

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    #interop_server_client = InteropClientConverter(MSL_ALT, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

    logger_queue = multiprocessing.Queue(-1)
    logger_listener_process = multiprocessing.Process(target=listener_process, args=(logger_queue, logger_listener_configurer))
    logger_listener_process.start()

    timestamped_location_data_array = manager.list()
    target_listener_process = multiprocessing.Process(target=target_listener, args=(logger_queue, logger_worker_configurer, timestamped_location_data_array))
    target_listener_process.start()

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
    #while len(vehicle.commands) < 1 and not vehicle.is_armable:
    #    sleep(0.05)

    log(name, "Downloading waypoints from UAV on: %s" % UAV_CONNECTION_STRING)
    waypoints = vehicle.commands
    waypoints.download()
    waypoints.wait_ready()
    log(name, "Waypoints successfully downloaded")

    log(name, "Enabling SDA...")
    sda_converter = SDAConverter(get_location(vehicle))
    sda_converter.set_waypoint(Location(38.8703041, -77.3214035, 100))
    #sda_converter.set_waypoint(Location(waypoints[0].x, waypoints[0].y, waypoints[0].z))
    log(name, "SDA enabled")
    gps_update_index = 0
    current_location = get_location(vehicle)
    timestamped_location_data_array.append({
        "index" : gps_update_index,
        "geo_stamp" : GeoStamp((current_location.get_lat(), current_location.get_lon()), datetime.now())
    })
    vehicle_state_data.append(get_vehicle_state(vehicle, sda_converter, MSL_ALT))
    stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
    obstacles_array = [stationary_obstacles, moving_obstacles]
    mission_data.append(get_mission_json(interop_server_client.get_active_mission(), obstacles_array))

    log(name, "Everything is instantiated...Beginning operation")
    #try:
    while True:
        current_location = get_location(vehicle)
        #current_waypoint_number = vehicle.commands.next
        #current_uav_waypoint = waypoints[current_waypoint_number]
        #sda_converter.set_waypoint(Location(current_uav_waypoint.x, current_uav_waypoint.y, current_uav_waypoint.z))

        interop_server_client.post_telemetry(current_location, vehicle.heading)
        gps_update_index += 1
        timestamped_location_data_array[0] = {
            "index" : gps_update_index,
            "geo_stamp" : GeoStamp((current_location.get_lat(), current_location.get_lon()), datetime.now())
        }
        stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
        obstacles_array = [stationary_obstacles, moving_obstacles]
        """sda_converter.reset_obstacles()
        for stationary_obstacle in stationary_obstacles:
            sda_converter.add_obstacle(get_obstacle_location(stationary_obstacle), stationary_obstacle)
        for moving_obstacle in moving_obstacles:
            sda_converter.add_obstacle(get_obstacle_location(moving_obstacle), moving_obstacle)"""

        vehicle_state_data[0] = get_vehicle_state(vehicle, sda_converter, MSL_ALT)
        mission_data[0] = get_mission_json(interop_server_client.get_active_mission(), obstacles_array)

        sleep(0.5)
        """if vehicle.mode.name == "GUIDED" and sda_converter.has_uav_reached_guided_waypoint():
            vehicle.mode = VehicleMode("AUTO")

        sda_converter.set_uav_position(current_location)

        obj_avoid_coordinates = sda_converter.avoid_obstacles(math.radians(vehicle.heading) / 2)
        print(current_location.get_altitude())
        if obj_avoid_coordinates:
            log("root", "Avoiding obstacles...")
            vehicle.simple_goto(obj_avoid_coordinates)"""
    #except:
    #    pass#vehicle.close()

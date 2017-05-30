from dronekit import connect, VehicleMode
import socket
import multiprocessing
from datetime import datetime
from logger import *
from time import sleep
from interop_client import InteropClientConverter
from sda_converter import SDAConverter
from converter_functions import *
from data_functions import *
from sda_viewer import SDAViewSocket
from SimpleWebSocketServer import SimpleWebSocketServer
from vehicle_state import VehicleState
from SDA import *
from ImgProcessingCLI.Runtime.RuntimeTarget import RuntimeTarget
from ImgProcessingCLI.DataMine.OrientationSolver import OrientationSolver
from ImgProcessingCLI.DataMine import KMeansCompare
from ImgProcessingCLI.Runtime import TargetCropper2
from EigenFit.DataMine import Categorizer
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
from ImgProcessingCLI.Runtime.GeoStamps import GeoStamps
from EigenFit.Load import *
from Runtime.TargetCrop import TargetCrop
from timeit import default_timer
import rawpy
import shutil
import PIL

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

def target_listener(logger_queue, configurer, timestamped_location_data_array):
    """
    Run targets and submit them to the interoperability server
    """
    configurer(logger_queue)
    name = multiprocessing.current_process().name

    interop_server_client = InteropClientConverter(MSL_ALT, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

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
    geo_stamps = GeoStamps(gps_coords)
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

                target_crops = TargetCropper2.get_target_crops_from_img2(rgb_image, geo_stamps, 6)
                target_crops = TargetCrop.get_non_duplicate_crops(all_target_crops, target_crops, client.MIN_DIST_BETWEEN_TARGETS_KM)
                all_target_crops.extend(target_crops)
                log(name, "Finished processing", pic_name, "in", str(default_timer() - start_time))

                for target_crop in target_crops:
                    log(name, "Identifying target characteristics of target #" + str(crop_index))
                    runtime_target = RuntimeTarget(target_crop, letter_categorizer, orientation_solver)
                    target_json_output = runtime_target.get_competition_json_output()

                    log(name, "Saving target characteristics of target #" + str(crop_index))
                    output_pic_name = os.path.join(GENERATED_DATA_LOCATION, "object_file_format", str(crop_index) + ".png")
                    output_json_name = os.path.join(GENERATED_DATA_LOCATION, "object_file_format", str(crop_index) + ".json")
                    save_json_data(output_json_name, target_json_output)

                    crop_index += 1
                '''have to submit generated data to interop server'''

def convert_fly_zones(fly_zones):
    """
    Wrapper method for converting a list of fly zones
    """
    converted_fly_zones = []
    for fly_zone in fly_zones:
        converted_fly_zones.append(convert_fly_zone(fly_zone))

    return converted_fly_zones

def convert_fly_zone(fly_zone):
    """
    Convert a fly zone (lat, lon) to (x, y)
    """
    converted_boundary_points = []
    for index in range(len(fly_zone)):
        for boundary_point in fly_zone:
            if boundary_point["order"] == index:
                converted_boundary_points.append(Location(boundary_point["latitude"], boundary_point["longitude"], 0))
                break

    return converted_boundary_points

def calculate_polygon_area(fly_zone):
    """
    Calculates the area of the polygon
    """
    x = fly_zone[:, 0]
    y = fly_zone[:, 1]

    return 0.5*numpy.abs(numpy.dot(x,numpy.roll(y,1))-numpy.dot(y,numpy.roll(x,1)))

def find_largest_flight_zone(fly_zones):
    """
    Find the largest fly zone out of the fly zones provided. They must be in XY
    coordinates
    """
    largest_fly_zone = fly_zones[0]
    largest_fly_zone_area = calculate_polygon_area(fly_zones[0])

    for fly_zone in fly_zones[1:]:
        test_fly_zone_area = calculate_polygon_area(fly_zone)

        if test_fly_zone_area > largest_fly_zone_area:
            largest_fly_zone_area = test_fly_zone_area
            largest_fly_zone = fly_zone

    return largest_fly_zone

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    interop_server_client = InteropClientConverter(MSL_ALT, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

    logger_queue = multiprocessing.Queue(-1)
    logger_listener_process = multiprocessing.Process(target=listener_process, args=(logger_queue, logger_listener_configurer))
    logger_listener_process.start()

    timestamped_location_data_array = manager.list()
    target_listener_process = multiprocessing.Process(target=target_listener, args=(logger_queue, logger_worker_configurer, timestamped_location_data_array))
    #target_listener_process.start()
    #target_listener(logger_queue, logger_worker_configurer, timestamped_location_data_array)
    #while True:
    #    sleep(0.5)

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
    #waypoints.wait_ready()
    log(name, "Waypoints successfully downloaded")

    gps_update_index = 0
    current_location = get_location(vehicle)
    timestamped_location_data_array.append({
        "index" : gps_update_index,
        "geo_stamp" : GeoStamp((current_location.get_lat(), current_location.get_lon()), datetime.now().strftime("%h %M %S"))
    })
    stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
    obstacles_array = [stationary_obstacles, moving_obstacles]
    mission_data.append(get_mission_json(interop_server_client.get_active_mission(), obstacles_array))

    fly_zones = mission_data[0]["fly_zones"]
    converted_fly_zones = convert_fly_zones(fly_zones)
    largest_fly_zone = find_largest_flight_zone(converted_fly_zones)

    log(name, "Enabling SDA...")
    sda_converter = SDAConverter(get_location(vehicle), largest_fly_zone)
    sda_converter.set_waypoint(Location(waypoints[1].x, waypoints[1].y, waypoints[1].z))
    log(name, "SDA enabled")

    vehicle_state_data.append(get_vehicle_state(vehicle, sda_converter, MSL_ALT))

    log(name, "Everything is instantiated...Beginning operation")
    #try:
    while True:
        current_location = get_location(vehicle)
        current_waypoint_number = vehicle.commands.next
        if current_waypoint_number != 0:
            current_uav_waypoint = waypoints[current_waypoint_number - 1]
            sda_converter.set_waypoint(Location(current_uav_waypoint.x, current_uav_waypoint.y, current_uav_waypoint.z * 3.28084))

        interop_server_client.post_telemetry(current_location, vehicle.heading)
        """gps_update_index += 1
        timestamped_location_data_array[0] = {
            "index" : gps_update_index,
            "geo_stamp" : GeoStamp((current_location.get_lat(), current_location.get_lon()), datetime.now())
        }"""
        stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
        obstacles_array = [stationary_obstacles, moving_obstacles]
        sda_converter.reset_obstacles()
        for stationary_obstacle in stationary_obstacles:
            sda_converter.add_obstacle(get_obstacle_location(stationary_obstacle), stationary_obstacle)
        """for moving_obstacle in moving_obstacles:
            sda_converter.add_obstacle(get_obstacle_location(moving_obstacle), moving_obstacle)"""

        vehicle_state_data[0] = get_vehicle_state(vehicle, sda_converter, MSL_ALT)
        mission_data[0] = get_mission_json(interop_server_client.get_active_mission(), obstacles_array)

        sda_converter.set_uav_position(current_location)
        sda_converter.avoid_obstacles()

        if (vehicle.location.global_relative_frame.alt * 3.28084) > 60:
            if not sda_converter.has_uav_completed_guided_path():
                log("root", "Avoiding obstacles...")
                print(sda_converter.get_uav_avoid_coordinates())
                vehicle.mode = VehicleMode("GUIDED")
                vehicle.simple_goto(sda_converter.get_uav_avoid_coordinates())

        if vehicle.mode.name == "GUIDED" and sda_converter.has_uav_completed_guided_path() and sda_converter.does_guided_path_exist():
            vehicle.mode = VehicleMode("AUTO")

        sleep(0.5)
    #except:
    #    while True:
    #        sleep(0.5)
    #    pass#vehicle.close()

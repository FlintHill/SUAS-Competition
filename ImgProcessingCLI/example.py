import multiprocessing
import exifread
import rawpy
import os
import shutil
import PIL
from PIL import Image
from datetime import datetime
from timeit import default_timer
from time import sleep
from SUASSystem import GCSSettings
from SUASSystem.suas_logging import log
from ImgProcessingCLI.Runtime.RuntimeTarget import RuntimeTarget
from ImgProcessingCLI.DataMine.OrientationSolver import OrientationSolver
from ImgProcessingCLI.DataMine import KMeansCompare
from ImgProcessingCLI.Runtime import TargetCropper3
from EigenFit.DataMine import Categorizer
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
from ImgProcessingCLI.Runtime.GeoStamps import GeoStamps
from EigenFit.Load import *
from ImgProcessingCLI.Runtime.TargetCrop import TargetCrop

def run_img_proc_process(logger_queue, img_proc_status, location_log, targets_to_submit):
    SUASSystem.logging.logger_worker_configurer(logger_queue)
    logger_name = multiprocessing.current_process().name

    log(logger_name, "Instantiating letter categorizer")
    eigenvectors = load_numpy_arr(GCSSettings.BASE_LETTER_CATEGORIZER_PCA_PATH + "/Data/Eigenvectors/eigenvectors 0.npy")
    projections_path = GCSSettings.BASE_LETTER_CATEGORIZER_PCA_PATH + "/Data/Projections"
    mean = load_numpy_arr(GCSSettings.BASE_LETTER_CATEGORIZER_PCA_PATH + "/Data/Mean/mean_img 0.npy")
    num_dim = 20
    letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, num_dim)
    log(logger_name, "Letter categorizer instantiated successfully")

    log(logger_name, "Instantiating orientation solver")
    orientation_eigenvectors = load_numpy_arr(GCSSettings.BASE_ORIENTATION_CLASSIFIER_PCA_PATH + "/Data/Eigenvectors/eigenvectors 0.npy")
    orientation_projections_path = GCSSettings.BASE_ORIENTATION_CLASSIFIER_PCA_PATH + "/Data/Projections"
    orientation_mean = load_numpy_arr(GCSSettings.BASE_ORIENTATION_CLASSIFIER_PCA_PATH + "/Data/Mean/mean_img 0.npy")
    orientation_num_dim = 50
    orientation_solver = OrientationSolver(orientation_eigenvectors, orientation_mean, GCSSettings.BASE_ORIENTATION_CLASSIFIER_PCA_PATH, orientation_num_dim)
    log(logger_name, "Orientation solver instantiated")

    if os.path.exists(GCSSettings.GENERATED_DATA_LOCATION):
        shutil.rmtree(GCSSettings.GENERATED_DATA_LOCATION)

    os.mkdir(GCSSettings.GENERATED_DATA_LOCATION)
    os.mkdir(os.path.join(GCSSettings.GENERATED_DATA_LOCATION, "object_file_format"))

    sd_path = os.path.join("/Volumes", GCSSettings.SD_CARD_NAME, "DCIM")
    gps_coords = []

    while True:
        if "enabled" in str(img_proc_status.value).lower():
                if len(location_log) != 0:
                    try:
                        gps_coords.append(location_log[0])
                        gps_coords = gps_coords[1:]
                    except:
                        pass

                log(logger_name, "Waiting for path to exist...")

                # Wait for SD card to be loaded
                if not os.path.exists(sd_path):
                    sleep(1)

                    continue

                # Once SD card is loaded, begin processing
                # For every image on the SD card
                # 1. Load the image
                # 2. Process the crops, determine the ones that are targets
                # 3. Save the targets to GENERATED_DATA_LOCATION
                # 4. Upload the targets to interop server
                log(logger_name, "Beginning image processing...")
                geo_stamps = GeoStamps([GeoStamp([38.38875, -77.27532], datetime.now())])#gps_coords)
                crop_index = 0

                all_target_crops = []
                for pic_folder in os.listdir(sd_path):
                    pictures_dir_path = os.path.join(sd_path, pic_folder)

                    for pic_name in os.listdir(pictures_dir_path):
                        if ".SRW" in pic_name:
                            start_time = default_timer()
                            log(logger_name, "Loading image " + pic_name)
                            pic_path = os.path.join(pictures_dir_path, pic_name)
                            img = rawpy.imread(pic_path).postprocess()
                            rgb_image = Image.fromarray(numpy.roll(img, 1, axis=0))
                            image_timestamp = get_image_timestamp(pic_path)

                            target_crops = TargetCropper3.get_target_crops_from_img(rgb_image, image_timestamp, geo_stamps, 6)
                            target_crops = TargetCrop.get_non_duplicate_crops(all_target_crops, target_crops, GCSSettings.MIN_DIST_BETWEEN_TARGETS_KM)
                            all_target_crops.extend(target_crops)
                            log(logger_name, "Finished processing " + pic_name + " in " + str(default_timer() - start_time) + " seconds")

                            for target_crop in target_crops:
                                try:
                                    log(logger_name, "Identifying target characteristics of target #" + str(crop_index))
                                    runtime_target = RuntimeTarget(target_crop, letter_categorizer, orientation_solver)
                                    target_json_output = runtime_target.get_competition_json_output()

                                    log(logger_name, "Saving target characteristics of target #" + str(crop_index))
                                    output_pic_name = os.path.join(GENERATED_DATA_LOCATION, "object_file_format", str(crop_index) + ".png")
                                    output_json_name = os.path.join(GENERATED_DATA_LOCATION, "object_file_format", str(crop_index) + ".txt")
                                    save_json_data(output_json_name, {"target_json_output" : "Testing"})#target_json_output)
                                    target_crop.get_crop_img().save(output_pic_name)

                                    crop_index += 1
                                except:
                                    log(logger_name, "ERROR: Could not process a target crop")

        sleep(0.5)

def get_image_timestamp(filename):
    """
    Returns an image's timestamp
    """
    opened_file = open(filename, 'rb')
    tags = exifread.process_file(opened_file)
    image_raw_time = tags['Image DateTime']
    converted_time = datetime.strptime(str(image_raw_time), "%Y:%m:%d %H:%M:%S")

    return converted_time

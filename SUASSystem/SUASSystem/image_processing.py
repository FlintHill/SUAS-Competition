from time import sleep
import os
from SUASSystem import utils

def run_img_proc_process(logger_queue, img_proc_status, location_log, targets_to_submit):
    while True:


        if len(targets_to_submit) > 0:
            target_characteristics=targets_to_submit.pop(0)
            original_image_path = "static/imgs/" + target_characteristics["base_image_filename"]
            cropped_target_path = "static/crops/" + str(len(os.listdir('static/crops'))) + ".jpg"
            cropped_target_data_path = "static/crops/" + str(len(os.listdir('static/crops'))) + ".json"
            utils.crop_target(original_image_path, cropped_target_path, target_characteristics["target_top_left"], target_characteristics["target_bottom_right"])
            utils.save_json_data(cropped_target_data_path, target_characteristics)

            location_log[0].post_standard_target(target_characteristics, cropped_target_path)

        sleep(0.1)

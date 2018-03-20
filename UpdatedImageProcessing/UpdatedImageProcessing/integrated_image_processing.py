import os
import time
import json
from PIL import Image
from .TargetDetection import *
from .ShapeDetection import *
from .Classifiers import *

class IntegratedImageProcessing(object):

    @staticmethod
    def run_integrated_image_processing(target_map_path, image_save_path, json_save_path):
        target_detected = []
        amount_of_target_maps_present = len(set(os.listdir(target_map_path))) - len(set(target_detected))

        while (amount_of_target_maps_present > 0):

            print "Target Maps Left to Detect: " + str(amount_of_target_maps_present)

            for index_1 in range(len(set(os.listdir(target_map_path)))):
                current_target_map_name = os.listdir(target_map_path)[index_1]

                is_current_target_map_detected = False
                for index_2 in range(len(target_detected)):
                    if (target_detected[index_2] == current_target_map_name):
                        is_current_target_map_detected = True

                if (is_current_target_map_detected == False):
                    target_detected.append(current_target_map_name)
                    break

            combo_target_detection_result_list = SingleTargetMapDetector.detect_single_target_map(os.path.join(target_map_path, current_target_map_name))
            single_target_crops = combo_target_detection_result_list[0]
            json_file = combo_target_detection_result_list[1]

            for index_3 in range(len(single_target_crops)):
                json_file["image_processing_results"][index_3]["target_index"] = index_3 + 1

                current_crop_path = os.path.join(image_save_path, current_target_map_name + " - " + str(index_3 + 1) + ".png")
                single_target_crops[index_3].save(current_crop_path)

                shape_type = ShapeClassificationTwo(current_crop_path).get_shape_type()
                json_file["image_processing_results"][index_3]["target_shape_type"] = shape_type

                color_classifying_results = ColorClassifier(current_crop_path).get_color()
                shape_color = color_classifying_results[0]
                letter_color = color_classifying_results[1]
                json_file["image_processing_results"][index_3]["target_shape_color"] = shape_color
                json_file["image_processing_results"][index_3]["target_letter_color"] = letter_color

            with open(os.path.join(json_save_path, current_target_map_name + ".json"), 'w') as fp:
                json.dump(json_file, fp, indent=4)

            amount_of_target_maps_present -= 1

import os
import timeit
import json
from ImageProcessing2.TargetDetection import *
from ImageProcessing2.TargetDetectionTester import *

#start_time = timeit.default_timer()

#Run UpdatedImageProcessing here. More parameters can be changed in target_detection_settings.py.

#Detect targets on all target maps in the given path
target_detected = []
target_map_path = "/Users/zyin/Desktop/Synthetic_Dataset/Answers/modular_target_maps"
autonomous_image_processing_save_path = "/Users/zyin/Desktop/Target_Detection_Report"

while True:
    amount_of_target_maps_present = len(set(os.listdir(target_map_path))) - len(set(target_detected))

    while (amount_of_target_maps_present > 0):
        current_target_map_name = ""

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
            single_target_crops[index_3].save(os.path.join(autonomous_image_processing_save_path, current_target_map_name + " - " + str(index_3 + 1) + ".png"))

        with open(os.path.join(autonomous_image_processing_save_path, current_target_map_name + ".json"), 'w') as fp:
            json.dump(json_file, fp, indent=4)

        amount_of_target_maps_present -= 1

        print amount_of_target_maps_present

    print "Run through completed"




'''
combo_target_detection_result_list = MassTargetDetector.detect_mass_target(os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps"))

Logger.format_time_report(timeit.default_timer() - start_time)

TargetDetectionResultSaver.save_target_detection_result(combo_target_detection_result_list)

AutomaticTester.run_automatic_tester()
'''

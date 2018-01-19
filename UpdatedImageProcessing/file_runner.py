import os
import timeit
import json
from ImageProcessing2.TargetDetection import *
from ImageProcessing2.TargetDetectionTester import *

#start_time = timeit.default_timer()

#Run UpdatedImageProcessing here. More parameters can be changed in target_detection_settings.py.

#Detect targets on all target maps in the given path

combo_target_detection_result_list = MassTargetDetector.detect_mass_target(os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps"))

Logger.format_time_report(timeit.default_timer() - start_time)

TargetDetectionResultSaver.save_target_detection_result(combo_target_detection_result_list)

AutomaticTester.run_automatic_tester()

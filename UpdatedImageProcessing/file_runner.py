<<<<<<< HEAD
import os
import timeit
import json
||||||| merged common ancestors
=======
import os
import timeit
>>>>>>> Separated the detection process from the testing process to prepare for the integration
from ImageProcessing2.TargetDetection import *
from ImageProcessing2.TargetDetectionTester import *

start_time = timeit.default_timer()

#Run UpdatedImageProcessing here. More parameters can be changed in target_detection_settings.py.

#Detect targets on all target maps in the given path
<<<<<<< HEAD
||||||| merged common ancestors
MassTargetDetector.detect_mass_target()
=======

combo_target_detection_result_list = MassTargetDetector.detect_mass_target(os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps"))
>>>>>>> Separated the detection process from the testing process to prepare for the integration

<<<<<<< HEAD
combo_target_detection_result_list = MassTargetDetector.detect_mass_target(os.path.expanduser("~/Desktop/Synthetic_Dataset/Answers/modular_target_maps"))

Logger.format_time_report(timeit.default_timer() - start_time)

TargetDetectionResultSaver.save_target_detection_result(combo_target_detection_result_list)

AutomaticTester.run_automatic_tester()
||||||| merged common ancestors
TargetDetectionLogger.format_time_report(timeit.default_timer() - start_time)
=======
TargetDetectionLogger.format_time_report(timeit.default_timer() - start_time)

TargetDetectionResultSaver.save_target_detection_result(combo_target_detection_result_list)

AutomaticTester.run_automatic_tester()
>>>>>>> Separated the detection process from the testing process to prepare for the integration

from ImageProcessing2.TargetDetection import *
from PIL import Image
import timeit

start_time = timeit.default_timer()

#Run UpdatedImageProcessing here. More parameters can be changed in target_detection_settings.py.

#Detect targets on all target maps in the given path
MassTargetDetector.detect_mass_target()

TargetDetectionLogger.format_time_report(imeit.default_timer() - start_time)

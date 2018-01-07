from ImageProcessing2.TargetDetection import *
from PIL import Image
import timeit

start_time = timeit.default_timer()

#Run UpdatedImageProcessing here. More parameters can be changed in target_detection_settings.py.

#Detect targets on all target maps in the given path
MassTargetDetector.detect_mass_target()

time_in_seconds = timeit.default_timer() - start_time
minutes = int(time_in_seconds / 60)
seconds = time_in_seconds - (minutes * 60)
print str(minutes) + "min " + str(seconds) + "s"

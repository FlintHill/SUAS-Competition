from ImageProcessing2.TargetDetection import *
import timeit

start = timeit.timeit()

#Run UpdatedImageProcessing here. More parameters can be changed in target_detection_settings.py.

#Detect targets on all target maps in the given path
MassTargetDetector.detect_mass_target()

end = timeit.timeit()
print end - start

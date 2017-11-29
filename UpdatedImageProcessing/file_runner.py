from TargetDetection import *
from PIL import Image

#Run UpdatedImageProcessing here. More parameters can be changed in target_detection_settings.py.

#Detect targets on all target maps in the given path
MassTargetDetector.detect_mass_target()

#map_image = Image.open("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps/11.jpg")

#TargetRebounder.rebound_target(map_image, (4041, 3286))

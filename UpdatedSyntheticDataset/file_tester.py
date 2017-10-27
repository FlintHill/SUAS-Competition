from SyntheticDataset2 import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import random

<<<<<<< HEAD


"""
target = SpecifiedTargetWithBackground("circle", "N", "A", (255, 255, 255, 255), (255, 0, 0, 255), 45)
target.create_specified_target_with_background().show()
target.record_specified_target_with_background("tester.txt")

target_map = TargetMap(10)
target_map.create_random_target_map().show()
target_map.record_random_target_map("test")
"""
SyntheticDatasetMaker.create_target_maps(1, 5)
SyntheticDatasetMaker.create_single_targets(3)
||||||| merged common ancestors


"""
target = SpecifiedTargetWithBackground("circle", "N", "A", (255, 255, 255, 255), (255, 0, 0, 255), 45)
target.create_specified_target_with_background().show()
target.record_specified_target_with_background("tester.txt")

target_map = TargetMap(10)
target_map.create_random_target_map().show()
target_map.record_random_target_map("test")
"""
#SyntheticDatasetMaker.create_target_maps(2, 5)
=======
SyntheticDatasetMaker.create_target_maps(2, 5)
>>>>>>> Changed logging outputs
#SyntheticDatasetMaker.create_single_targets(5)

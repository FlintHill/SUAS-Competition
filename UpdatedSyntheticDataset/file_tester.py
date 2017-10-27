from SyntheticDataset2 import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import random



"""
target = SpecifiedTargetWithBackground("circle", "N", "A", (255, 255, 255, 255), (255, 0, 0, 255), 45)
target.create_specified_target_with_background().show()
target.record_specified_target_with_background("tester.txt")

target_map = TargetMap(10)
target_map.create_random_target_map().show()
target_map.record_random_target_map("test")
"""
#SyntheticDatasetMaker.create_target_maps(2, 5)
#SyntheticDatasetMaker.create_single_targets(5)
SyntheticDatasetMaker.create_synthetic_dataset(2, 10, 10)

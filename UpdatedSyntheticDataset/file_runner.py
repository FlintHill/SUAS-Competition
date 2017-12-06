from SyntheticDataset2 import *

#Run UpdatedSyntheticDataset here. More parameters can be changed in ImageCreator/settings.py.

#Input (number of maps to create, number of targets on each map)
SyntheticDatasetMaker.create_target_maps(4, 10, "randomize", "randomize", "randomize", "randomize", "randomize", "randomize")

#Input (number of single targets to create)
SyntheticDatasetMaker.create_single_targets(4, "randomize", "randomize", "randomize", "randomize", "randomize", "randomize")

from SyntheticDataset2 import *

#Run UpdatedSyntheticDataset here. More parameters can be changed in ImageCreator/settings.py.

#Input (number of maps to create, number of targets on each map)
ModularSyntheticDatasetMaker.create_modular_target_maps(0, 0)

#Input (number of single targets with background to create)
ModularSyntheticDatasetMaker.create_modular_single_targets_with_background(50)

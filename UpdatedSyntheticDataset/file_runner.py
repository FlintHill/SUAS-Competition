from SyntheticDataset2 import *

#Run UpdatedSyntheticDataset here. More parameters can be changed in ImageCreator/settings.py.
"""
#Input (number of maps to create, number of targets on each map)
RandomSyntheticDatasetMaker.create_random_target_maps(4, 10)

#Input (number of single targets with background to create)
RandomSyntheticDatasetMaker.create_random_single_targets_with_background(4)

#Input (number of single targets without background to create)
RandomSyntheticDatasetMaker.create_random_single_targets_without_background(4)
"""
#Input (number of maps to create, number of targets on each map)
ModularSyntheticDatasetMaker.create_modular_target_maps(4, 10)

#Input (number of single targets with background to create)
#ModularSyntheticDatasetMaker.create_modular_single_targets_with_background(4)

#Input (number of single targets without background to create)
#ModularSyntheticDatasetMaker.create_modular_single_targets_without_background(4)

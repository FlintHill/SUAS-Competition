from SyntheticDataset2 import *

"""
Run UpdatedSyntheticDataset here. More parameters can be changed in ImageCreator/settings.py.
"""

SyntheticDatasetMaker.create_target_maps(10, 10)
"""Input (number of maps to create, number of targets on each map)"""

SyntheticDatasetMaker.create_single_targets(0)
"""Input (number of single targets to create)"""

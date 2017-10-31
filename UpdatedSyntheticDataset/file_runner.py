from SyntheticDataset2 import *

"""
Run UpdatedSyntheticDataset here. More parameters can be changed in ImageCreator/settings.py.
"""

SyntheticDatasetMaker(2, 5, 3).create_target_maps()
"""Input (number of maps to create, number of targets on each map)"""

SyntheticDatasetMaker(2, 5, 3).create_single_targets()
"""Input (number of single targets to create)"""

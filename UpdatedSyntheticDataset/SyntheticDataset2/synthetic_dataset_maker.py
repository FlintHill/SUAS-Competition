import os
from SyntheticDataset2.ImageCreator import *

class SyntheticDatasetMaker(object):

    @staticmethod
    def create_target_maps(number_of_target_maps, number_of_targets_on_each_map):
        if (os.path.isdir(Settings.SAVE_PATH + "/target_maps")):
            raise Exception("Cannot create Target Maps: Save directory already exists")

        if (os.path.isdir(Settings.SAVE_PATH + "/target_maps_answers")):
            raise Exception("Cannot create Target Maps Answers: Save directory already exists")

        os.mkdir(Settings.SAVE_PATH + "/target_maps")
        os.mkdir(Settings.SAVE_PATH + "/target_maps_answers")

        target_maps = []

        for index in range(number_of_target_maps):
            target_map = TargetMap(number_of_targets_on_each_map)
            target_maps.append(target_map.create_random_target_map())
            target_map.record_random_target_map(index+1)

        return target_maps

    @staticmethod
    def create_single_targets(number_of_single_targets):
        if (os.path.isdir(Settings.SAVE_PATH + "/single_targets")):
            raise Exception("Cannot create Single Targets: Save directory already exists")
        if (os.path.isdir(Settings.SAVE_PATH + "/single_targets_answers")):
            raise Exception("Cannot create Single Targets Answers: Save directory already exists")

        os.mkdir(Settings.SAVE_PATH + "/single_targets")
        os.mkdir(Settings.SAVE_PATH + "/single_targets_answers")

        single_targets = []

        for index in range(number_of_single_targets):
            single_target = RandomTargetWithBackground()
            single_targets.append(single_target.create_random_target_with_background())
            single_target.record_random_target_with_background(index+1)

        return single_targets

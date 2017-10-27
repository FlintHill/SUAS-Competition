import os
from SyntheticDataset2.ImageCreator import *

class SyntheticDatasetMaker(object):

    @staticmethod
    def create_synthetic_dataset(number_of_target_maps, number_of_targets_on_each_map, number_of_single_targets):
        synthetic_dataset = []

        for index in range(number_of_target_maps):
            target_map = TargetMap(number_of_targets_on_each_map)
            synthetic_dataset.append(target_map.create_random_target_map())
            target_map.record_random_target_map()
            os.rename(Settings.TEXT_SAVING_PATH + "/tester.txt", Settings.TEXT_SAVING_PATH + "/target_map_" + str(index + 1) + ".txt")
            os.rename(Settings.IMAGE_SAVING_PATH + "/tester.PNG", Settings.IMAGE_SAVING_PATH + "/target_map_" + str(index + 1) + ".PNG")

        for index in range(number_of_single_targets):
            single_target = RandomTargetWithBackground()
            synthetic_dataset.append(single_target.create_random_target_with_background())
            single_target.record_random_target_with_background()
            os.rename(Settings.TEXT_SAVING_PATH + "/tester.txt", Settings.TEXT_SAVING_PATH + "/single_target_" + str(index + 1) + ".txt")
            os.rename(Settings.IMAGE_SAVING_PATH + "/tester.PNG", Settings.IMAGE_SAVING_PATH + "/single_target_" + str(index + 1) + ".PNG")

        return synthetic_dataset

    @staticmethod
    def create_target_maps(number_of_target_maps, number_of_targets_on_each_map):
        target_maps = []

        for index in range(number_of_target_maps):
            target_map = TargetMap(number_of_targets_on_each_map)
            target_maps.append(target_map.create_random_target_map())
            target_map.record_random_target_map()
            os.rename(Settings.TEXT_SAVING_PATH + "/tester.txt", Settings.TEXT_SAVING_PATH + "/target_map_" + str(index + 1) + ".txt")
            os.rename(Settings.IMAGE_SAVING_PATH + "/tester.PNG", Settings.IMAGE_SAVING_PATH + "/target_map_" + str(index + 1) + ".PNG")

        return target_maps

    @staticmethod
    def create_single_targets(number_of_single_targets):
        single_targets = []

        for index in range(number_of_single_targets):
            single_target = RandomTargetWithBackground()
            single_targets.append(single_target.create_random_target_with_background())
            single_target.record_random_target_with_background()
            os.rename(Settings.TEXT_SAVING_PATH + "/tester.txt", Settings.TEXT_SAVING_PATH + "/single_target_" + str(index + 1) + ".txt")
            os.rename(Settings.IMAGE_SAVING_PATH + "/tester.PNG", Settings.IMAGE_SAVING_PATH + "/single_target_" + str(index + 1) + ".PNG")

        return single_targets

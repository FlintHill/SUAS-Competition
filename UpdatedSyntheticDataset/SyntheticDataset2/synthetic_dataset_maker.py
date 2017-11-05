import os, multiprocessing, timeit
from SyntheticDataset2.ImageCreator import *
from SyntheticDataset2.logger import Logger

class SyntheticDatasetMaker(object):

    @staticmethod
    def run_target_maps_generator(number_of_target_maps, number_of_targets_on_each_map, process_number):
        for index in range(number_of_target_maps):
            target_map = TargetMap(number_of_targets_on_each_map)
            target_map.create_random_target_map()
            Logger.log("Current process: " + str((process_number / number_of_target_maps) + 1) + "\n")
            target_map.record_random_target_map(process_number + index + 1)

    @staticmethod
    def create_target_maps(number_of_target_maps, number_of_targets_on_each_map):
        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY)):
            pass
        else:
            os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY)

        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps")):
            raise Exception("Cannot create Target Maps: Save directory already exists")
        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps_answers")):
            raise Exception("Cannot create Target Maps Answers: Save directory already exists")
        os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps")
        os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps_answers")

        cpu_count = multiprocessing.cpu_count()
        pics_per_process = (number_of_target_maps/cpu_count) + 1
        start_time = timeit.default_timer()

        jobs = []
        for index in range(cpu_count):
            starting_index = index * int(pics_per_process)
            image_generation_process = multiprocessing.Process(target=SyntheticDatasetMaker.run_target_maps_generator, args=(pics_per_process, number_of_targets_on_each_map, starting_index))
            jobs.append(image_generation_process)
            image_generation_process.start()

        for job in jobs:
            job.join()

        Logger.log("Target Maps saved at: " + Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps\n")
        Logger.log("Target Maps Answers saved at: " + Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps_answers\n")

        print("====================================")
        print("Total number of target_maps generated:", len(os.listdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps")))
        print("Total elapsed time (sec):", timeit.default_timer() - start_time)
        print("====================================")

    @staticmethod
    def run_single_targets_generator(number_of_single_targets, process_number):
        for index in range(number_of_single_targets):
            single_target = RandomTargetWithBackground()
            single_target.create_random_target_with_background()
            Logger.log("Current process: " + str((process_number / number_of_single_targets) + 1) + "\n")
            single_target.record_random_target_with_background(process_number + index + 1)

    @staticmethod
    def create_single_targets(number_of_single_targets):
        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY)):
            pass
        else:
            os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY)

        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets")):
            raise Exception("Cannot create Single Targets: Save directory already exists")
        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets_answers")):
            raise Exception("Cannot create Single Targets Answers: Save directory already exists")

        os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets")
        os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets_answers")

        cpu_count = multiprocessing.cpu_count()
        pics_per_process = (number_of_single_targets/cpu_count) + 1
        start_time = timeit.default_timer()

        jobs = []
        for index in range(cpu_count):
            starting_index = index * int(pics_per_process)
            image_generation_process = multiprocessing.Process(target=SyntheticDatasetMaker.run_single_targets_generator, args=(pics_per_process,starting_index))
            jobs.append(image_generation_process)
            image_generation_process.start()

        for job in jobs:
            job.join()

        Logger.log("Single Targets saved at: " + Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets\n")
        Logger.log("Single Targets Answers saved at: " + Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets_answers\n")

        print("====================================")
        print("Total number of single_targets generated:", len(os.listdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets")))
        print("Total elapsed time (sec):", timeit.default_timer() - start_time)
        print("====================================")

import os, multiprocessing, timeit
from SyntheticDataset2.ImageCreator import *
from SyntheticDataset2.logger import Logger

class ModularSyntheticDatasetMaker(object):

    @staticmethod
    def run_modular_target_maps_generator(number_of_target_maps, number_of_targets_on_each_map, process_number):
        for index in range(number_of_target_maps):
            target_map = ModularTargetMap(number_of_targets_on_each_map)
            target_map.create_modular_target_map()
            Logger.log("Current process: " + str((process_number / number_of_target_maps) + 1) + "\n")
            target_map.record_modular_target_map(process_number + index + 1)

    @staticmethod
    def create_modular_target_maps(number_of_target_maps, number_of_targets_on_each_map):
        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY)):
            pass
        else:
            os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY)

        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_target_maps")):
            raise Exception("Cannot create Modular Target Maps: Save directory already exists")
        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_target_maps_answers")):
            raise Exception("Cannot create Modular Target Maps Answers: Save directory already exists")
        os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_target_maps")
        os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_target_maps_answers")

        cpu_count = multiprocessing.cpu_count()
        pics_per_process = (number_of_target_maps / cpu_count) + 1
        start_time = timeit.default_timer()

        jobs = []
        for index in range(cpu_count):
            starting_index = index * int(pics_per_process)
            image_generation_process = multiprocessing.Process(target=ModularSyntheticDatasetMaker.run_modular_target_maps_generator, args=(pics_per_process, number_of_targets_on_each_map, starting_index))
            jobs.append(image_generation_process)
            image_generation_process.start()

        for job in jobs:
            job.join()

        Logger.log("Modular Target Maps saved at: " + Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_target_maps")
        Logger.log("Modular Target Maps Answers saved at: " + Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_target_maps_answers\n")

        print("====================================")
        print("Total number of modular target maps generated:", len(os.listdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_target_maps")))
        print("Total elapsed time (sec):", timeit.default_timer() - start_time)
        print("====================================")

    @staticmethod
    def run_modular_single_targets_with_background_generator(number_of_single_targets_with_background, process_number):
        for index in range(number_of_single_targets_with_background):
            single_target = ModularTargetWithBackground()
            single_target.create_modular_target_with_background()
            Logger.log("Current process: " + str((process_number / number_of_single_targets_with_background) + 1) + "\n")
            single_target.record_modular_target_with_background(process_number + index + 1)

    @staticmethod
    def create_modular_single_targets_with_background(number_of_single_targets_with_background):
        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY)):
            pass
        else:
            os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY)

        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background")):
            raise Exception("Cannot create Modular Single Targets With Background: Save directory already exists")
        if (os.path.isdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background_answers")):
            raise Exception("Cannot create Modular Single Targets With Background Answers: Save directory already exists")

        os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background")
        os.mkdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background_answers")

        cpu_count = multiprocessing.cpu_count()
        pics_per_process = (number_of_single_targets_with_background / cpu_count) + 1
        start_time = timeit.default_timer()

        jobs = []
        for index in range(cpu_count):
            starting_index = index * int(pics_per_process)
            image_generation_process = multiprocessing.Process(target=ModularSyntheticDatasetMaker.run_modular_single_targets_with_background_generator, args=(pics_per_process, starting_index))
            jobs.append(image_generation_process)
            image_generation_process.start()

        for job in jobs:
            job.join()

        Logger.log("Modular Single Targets With Background saved at: " + Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background")
        Logger.log("Modular Single Targets With Background Answers saved at: " + Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background_answers\n")

        print("====================================")
        print("Total number of modular single targets with background generated:", len(os.listdir(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background")))
        print("Total elapsed time (sec):", timeit.default_timer() - start_time)
        print("====================================")

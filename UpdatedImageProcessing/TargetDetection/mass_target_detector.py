import os, multiprocessing, timeit
from .target_detection_settings import TargetDetectionSettings
from .target_detection_logger import TargetDetectionLogger
from .blob_detector import BlobDetector
from .false_positive_eliminator import FalsePositiveEliminator
from .automatic_tester import AutomaticTester

def run_target_detector(target_map_path):

    positive_list = BlobDetector(target_map_path).detect_blobs()
    if (len(positive_list) > 15):
        positive_list = FalsePositiveEliminator.eliminate_overrepeated_colors(target_map_path, positive_list)

    positive_list = FalsePositiveEliminator.eliminate_overlapping_blobs(positive_list)
    positive_list = FalsePositiveEliminator.eliminate_by_surrounding_color(target_map_path, positive_list)
    print positive_list
    #return AutomaticTester(positive_list, self.target_map_answer_path).run_automatic_tester()

class MassTargetDetector(object):

    @staticmethod
    def detect_mass_target():
        target_maps_list = []
        target_map_answers_list = []
        for index in range(1, TargetDetectionSettings.NUMBER_OF_TARGET_MAPS + 1):
            target_maps_list.append(TargetDetectionSettings.TARGET_MAPS_DIRECTORY + "/" + str(index) + ".jpg")
            target_map_answers_list.append(TargetDetectionSettings.TARGET_MAPS_ANSWERS_DIRECTORY + "/" + str(index) + ".json")

        pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
        maps_per_process = TargetDetectionSettings.NUMBER_OF_TARGET_MAPS / multiprocessing.cpu_count()
        pool.map(run_target_detector, target_maps_list)

        """
        start_time = timeit.default_timer()

        jobs = []
        for index in range(cpu_count):
            starting_index = index * int(maps_per_process)
            target_detection_process = multiprocessing.Process(target=MassTargetDetector.run_mass_target_detector, args=(maps_per_process, starting_index))
            jobs.append(target_detection_process)
            target_detection_process.start()

        for job in jobs:
            job.join()

        TargetDetectionLogger.log("Target Detection Results saved at: " + TargetDetectionSettings.TARGET_DETECTION_SAVE_PATH)

        print("====================================")
        print("Total number of target_maps detected:", len(os.listdir(TargetDetectionSettings.TARGET_DETECTION_SAVE_PATH)))
        print("Total elapsed time (sec):", timeit.default_timer() - start_time)
        print("====================================")
        """


    @staticmethod
    def run_mass_target_detector():
        true_positives_count = 0
        false_positives_count = 0
        false_positives_list = []

        for index in range(1, TargetDetectionSettings.NUMBER_OF_TARGET_MAPS + 1):

            current_target_map = TargetDetectionSettings.TARGET_MAPS_DIRECTORY + "/" + str(index) + ".jpg"
            current_target_map_answers = TargetDetectionSettings.TARGET_MAPS_ANSWERS_DIRECTORY + "/" + str(index) + ".json"

            positive_list = TargetDetector.detect_targets(current_target_map)
            combo_positive_list = AutomaticTester.run_automatic_tester(positive_list, current_target_map_answers)

            true_positives_count += len(combo_positive_list[0])
            false_positives_count += len(combo_positive_list[1])

            if (len(combo_positive_list[1]) > 0):
                false_positives_list.append([index, combo_positive_list[1]])
            print index

        print str(float(true_positives_count) / (float(TargetDetectionSettings.NUMBER_OF_TARGET_MAPS) * 10) * 100) + "%"
        print str(false_positives_count)
        print false_positives_list

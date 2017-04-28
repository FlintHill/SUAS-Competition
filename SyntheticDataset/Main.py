from SyntheticDataset.image_operations import *
from SyntheticDataset.color import *
import math
import multiprocessing
import timeit
import os

DATA_PATH = "/Users/vtolpegin/github/SUAS-Competition/SyntheticDataset/data"
SAVE_PATH = "/Users/vtolpegin/github/SUAS-Competition/SyntheticDataset/Generated_Full_Targets"
TOTAL_GENERATED_TARGETS = 2
NUM_PICS_PER_TARGET = 10

def run_image_generator(process_number, num_pics, starting_index):
    generator = ImageGenerator(DATA_PATH, process_number=process_number)

    # NOTE: Only leave one of the two sets of code uncommented
    # NOTE: Uncomment the following two lines to generate polygon pics
    #generator.fillPolyPics(int(num_pics), starting_index)
    #generator.savePolyPicImgs(SAVE_PATH)

    # NOTE: Uncomment the following two lines to generate full synthetic images
    generator.generate_synthetic_images(int(num_pics), NUM_PICS_PER_TARGET, starting_index)
    generator.save_synthetic_images(SAVE_PATH)

if __name__ == '__main__':
    cpu_count = multiprocessing.cpu_count()
    # NOTE: Uncomment the following line to make the program run single threaded
    #cpu_count = 1
    pics_per_process = (TOTAL_GENERATED_TARGETS / cpu_count) + 1
    start_time = timeit.default_timer()

    jobs = []
    for index in range(cpu_count):
        starting_index = index * int(pics_per_process)
        image_generation_process = multiprocessing.Process(target=run_image_generator, args=(index, pics_per_process, starting_index))
        jobs.append(image_generation_process)
        image_generation_process.start()

    for job in jobs:
        job.join()

    print("====================================")
    print("Total number of images generated:", len(os.listdir(os.path.join(SAVE_PATH, "Images"))))
    print("Total elapsed time (sec):", timeit.default_timer() - start_time)
    print("====================================")

import SUASSystem
import multiprocessing
from time import sleep
from SUASSystem.logging import log

def run_img_proc_process(logger_queue, img_proc_status, targets_to_submit):
    SUASSystem.logging.logger_worker_configurer(logger_queue)
    logger_name = multiprocessing.current_process().name

    while True:
        if "enabled" in str(img_proc_status.value).lower():
            pass#log(logger_name, "IMG PROC ENABLED")
        elif "disabled" in str(img_proc_status.value).lower():
            pass#log(logger_name, "IMG PROC DISABLED")

        sleep(0.5)

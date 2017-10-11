from time import sleep

def run_img_proc_process(logger_queue, img_proc_status, location_log, targets_to_submit):
    while True:
        sleep(0.1)

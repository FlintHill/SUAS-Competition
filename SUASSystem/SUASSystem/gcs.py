from time import sleep
from .settings import GCSSettings

def gcs_process(sda_status, img_proc_status, interop_position_update_rate):
    while True:
        interop_position_update_rate.value += 1

        sleep(0.1)

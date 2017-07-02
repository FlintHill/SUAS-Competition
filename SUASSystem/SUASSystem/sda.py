from time import sleep

def run_sda_process(sda_status, sda_avoid_coords, mission_information_data):
    while True:
        if "enabled" in str(sda_status.value).lower():
            print("SDA ENABLED")
        elif "disabled" in str(sda_status.value).lower():
            print("SDA DISABLED")

        sleep(0.5)

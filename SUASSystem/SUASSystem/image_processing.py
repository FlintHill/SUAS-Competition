from time import sleep

def run_img_proc_process(img_proc_status, targets_to_submit):
    while True:
        if "enabled" in str(img_proc_status.value).lower():
            print("IMG PROC ENABLED")
        elif "disabled" in str(img_proc_status.value).lower():
            print("IMG PROC DISABLED")

        sleep(0.5)

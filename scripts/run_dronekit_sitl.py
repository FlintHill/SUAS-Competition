import dronekit_sitl
from time import sleep

"""
runs dronekit which is necessary for connecting to the Mission planner simulator. 
"""

if __name__ == '__main__':
    sitl = dronekit_sitl.start_default(lat=38.145206, lon=-76.428473)
    print("Connection String:", sitl.connection_string())

    try:
        while True:
            sleep(1)
    except:
        sitl.stop()

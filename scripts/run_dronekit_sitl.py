import dronekit_sitl
from time import sleep

if __name__ == '__main__':
    sitl = dronekit_sitl.start_default(lat=38.1452057, lon=-76.4281082)
    print("Connection String:", sitl.connection_string())

    try:
        while True:
            sleep(1)
    except:
        sitl.stop()

import dronekit
import time
import SUASSystem
from time import sleep
from SUASSystem import settings
from SUASSystem import converter_functions
from SUASSystem import gcs
from settings import GCSSettings


def connect_to_rover():
    print("Connecting to rover")
    rover = dronekit.connect(GCSSettings.UGV_CONNECTION_STRING, wait_ready=True)
    rover.wait_ready('autopilot_version')
    print("Connected to rover")

    return rover


def has_rover_reached_airdrop(r):
    rover_location = converter_functions.get_location(r)
    print(rover_location)

    lat_from_drop = abs(GCSSettings.AIRDROP_POINT_SCHOOL[0][0] - rover_location.get_lat())
    lon_from_drop = abs(GCSSettings.AIRDROP_POINT_SCHOOL[0][1] - rover_location.get_lon())
    print("Latitude from Drop: " + str(lat_from_drop))
    print("Longitude from Drop: " + str(lon_from_drop) + "\n")

    if (rover_location.get_alt() < 10 and rover_location.get_alt() > -1
    and lat_from_drop < 0.00035 and lon_from_drop < 0.00035):
        return True
    else:
        return False


def airdrop_countdown(wait):
    print("Rover Has Reached AirDrop")
    for x in range(wait):
        print("Rover Arming in: " + str(wait-x) + " seconds")
        sleep(1)



rover = connect_to_rover()

landed = False
while not landed:
    if (has_rover_reached_airdrop(rover)):
        landed = True

airdrop_countdown(120) #Change wait period (In seconds) here
rover.armed = True
print("Rover is Armed")
rover.mode = dronekit.VehicleMode("AUTO")
print("Rover Mode: AUTO")

import dronekit
import time
import SUASSystem
from time import sleep
from SUASSystem import settings
from SUASSystem import converter_functions
from SUASSystem import gcs
from settings import GCSSettings

def has_rover_reached_airdrop(rover):
    landed = False

    while not landed:
        rover_location = converter_functions.get_location(rover)
        print(rover_location)

        lat_from_drop = abs(GCSSettings.AIRDROP_POINT_SCHOOL[0][0] - rover_location.get_lat()) #AIRDROP
        lon_from_drop = abs(GCSSettings.AIRDROP_POINT_SCHOOL[0][1] - rover_location.get_lon())
        print("Latitude from Drop: " + str(lat_from_drop))
        print("Longitude from Drop: " + str(lon_from_drop) + "\n")

        if (rover_location.get_alt() < 10 and rover_location.get_alt() > -1
        and lat_from_drop < 0.00027 and lon_from_drop < 0.00027):
            print("Rover Has Reached AirDrop")
            sleep(30)
            rover.armed = True
            rover.mode = dronekit.VehicleMode("AUTO")
            landed = True;
            
rover = gcs.connect_to_rover()
has_rover_reached_airdrop()

SDA, An Overview


Beginning in GCS

SDA begins in GCS, when the process is initialized with the initialize_sda_process() method.
This method passes these variables to the SDA.py file in this exact order:
logger_queue, sda_status, UAV_status, waypoints, sda_avoid_coords, vehicle_state_data, mission_information_data
However, before we go into the SDA.py file, let's analyze exactly what the GCS.py file does.
In GCS.py, the SDA world begins with an if statement that checks whether or not the UAVs altitude
is greater than the SDA_MIN_ALT, and that SDA has been connected in the Web UI. In that if loop,
it checks whether or not the UAV_status(explained in the SDA file) is either GUIDED or AUTO. If
UAV_status is set to GUIDED, the vehicle's mode will be set to GUIDED and it will be told to go
to the SDA made avoid coordinates. However, if UAV_status is in AUTO and the vehicle mode is in
GUIDED, the vehicle's mode will be set to AUTO. If you have noticed, the vehicle's mode is dependent
on the UAV_status created by the code in SDA. At the end of the SDA portion in GCS.py, a safety if-loop
is written which sets the vehicle's mode to AUTO if it is not connected to interop and not already in AUTO.


Moving onto SDA.py

The first thing SDA.py tries to accomplish is the instantiation of SDAConverter. Again, we pass
these variables in this order (vehicle_state_data[0].get_location(), mission_information_data[0]["fly_zones"]) to the
SUASSystem.SDAConverter() method in order to instantiate the process. After SDAConverter is instantiated, a While True
loop starts whose purpose is to constantly check whether or not the UAV should be checking for obstacles, and then calling
the correct methods based on the circumstances. After saving the values of the current location and waypoint number,
an if-loop starts that checks if the next waypoint is avoidable (not a RTL, water drop, etc...) and if the UAV is
at the saved current location. If it passes those two conditions, SDA.py uses the sda_converter.py file to reset
all the obstacles, and then add them back to the obstacle map. If the UAV is not in GUIDED (GUIDED means its already
avoiding an obstacle), then it will run the avoid_obstacles method and create a guided path if one is necessary. If
it creates a guided path and has not completed it yet, the sda_converter.has_uav_completed_guided_path() will return False
and set the UAV_status to GUIDED while also setting sda_avoid_coords[0]. However, if it has completed its guided path,
UAV_status will be set to AUTO and the current path will be reset (meaning that the drone will go back to its preset path).


How it basically works in real time:

-Drone starts up
-Gets to competition height
-Begins checking for obstacles
-If overlapping obstacles exist, code combines them into the most efficient single obstacles
-Only cares if obstacles are in bounds and in path
-Creates 8 avoidance coordinates in obstacle_map based on obstacles location if it intersects the path
-Follows the shortest path
-Turns back to AUTO once path is complete


Downfalls

-Not 100% success rate when multiple separate obstacles in between two waypoints
-Waypoints inside obstacles have not been solved
-Moving obstacles as a whole


Other Important Files
  Read the methods in these files and their descriptions to understand the two main files better

obstacle_map.py
sda_converter.py

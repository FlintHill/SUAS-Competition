"""
	test drone control script
		less crashy, more fly-y

	@version	1.0
	@project	sense, detect, avoid
	@authors	jack harrington, james villemarette, vale tolpegin
	@date		4-10-2016
"""
import sys, logging, clr, time, MissionPlanner
clr.AddReference("MissionPlanner.Utilities")

# CLASS
class Obstacle:
	"""
	ADD SPEED FUNCTION AND SUCH
	"""
	lat = 0
	lng = 0
	alt = 0

	def __init__(self, latitude, longitude, altitude):
		lat = latitude
		lng = longitude
		alt = altitude

	def getLat(self):
		return lat

	def getLng(self):
		return lng

	def getAlt(self):
		return alt

# VARIABLES

drone_radius = 5 # meters

# FUNCTIONS
def new_waypoint(lat, lng, alt):
	"""
	Send a new waypoint in guided mode to go to
	"""
	item = MissionPlanner.Utilities.Locationwp()
	MissionPlanner.Utilities.Locationwp.lat.SetValue(item, lat)
	MissionPlanner.Utilities.Locationwp.lng.SetValue(item, lng)
	MissionPlanner.Utilities.Locationwp.alt.SetValue(item, alt)
	MAV.setGuidedModeWP(item)
	print "Waypoint which is LAT:%s LONG:%s ALT:%s" % (lat, lng, alt)

def meters_to_feet(m):
	"""
	Convert meters to feet
	"""
	return m * 3.28

def feet_to_meters(ft):
	"""
	Convert feet to meters
	"""
	return ft / 3.28

def reach_waypoint(lat, lng, alt, range, altrange):
	"""
	Stalls script until the drone reaches a certain lat, long, and altitude within a range
		range = latitude, longitude range
		altrange = altitude range
	"""
	while True:
		print cs.lat - lat
		print cs.lng - lng
		print cs.alt - alt
		if abs(cs.lat - lat) < range and abs(cs.lng - lng) < range and abs(cs.alt - alt) < altrange:
			return True
		time.sleep(0.1)

def calculate():
	"""
	Calculates within a 3D space if the drone will collide 
	"""

def calculate_entity_path():
	"""

	"""

def draw_obstacle(id, lat, lng, alt):
	"""
	Draws or redraws (updates) an obstacle on Mission Planner
	"""

def dodge_stationary():
	"""
	
	"""

def dodge_motion():
	"""

	"""

# RUNTIME CODE
"""
while True:
	if calculate():
		# if a collision is imminent
		#x
	else
		# if no collision is present
		time.sleep(100)
"""

# SETUP
print "Starting Mission"

Script.ChangeMode("Guided")

print "Guided Mode"

 # CREATING WAYPOINTS
lat = 38.871295
lng = -77.320000
alt = feet_to_meters(100.0)

new_waypoint(lat, lng, alt)
reach_waypoint(lat, lng, meters_to_feet(alt), 0.0002, 3)

print "Reached waypoint"

Script.ChangeMode("Auto")

print "Auto Mode"

print "End of Script"
time.sleep(99999)
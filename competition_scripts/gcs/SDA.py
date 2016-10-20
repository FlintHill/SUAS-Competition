"""
	test drone control script
		less crashy, more fly-y

	@version	1.0
	@project	sense, detect, avoid
	@authors	jack harrington, james villemarette, vale tolpegin
	@date		4-10-2016
"""
import sys, thread, logging, clr, time, MissionPlanner
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
safety_radius = 5 # for all obstacles

# FUNCTIONS
def reportTelemetry(threadName, delay):
	"""
	Post to the interoptclient.py our current position
	"""
	# something should be replaced with link to interopclient.py
	# something.post_telemetry(self, cs.lat, cs.lng, cs.alt, cs.yaw)
	# print "Reported Position"
	# time.sleep(delay)

def newWaypoint(lat, lng, alt):
	"""
	Send a new waypoint in guided mode to go to
	"""
	item = MissionPlanner.Utilities.Locationwp()
	MissionPlanner.Utilities.Locationwp.lat.SetValue(item, lat)
	MissionPlanner.Utilities.Locationwp.lng.SetValue(item, lng)
	MissionPlanner.Utilities.Locationwp.alt.SetValue(item, alt)
	MAV.setGuidedModeWP(item)
	print "Waypoint which is LAT:%s LONG:%s ALT:%s" % (lat, lng, alt)

def metersToFeet(m):
	"""
	Convert meters to feet
	"""
	return m * 3.28

def feetToMeters(ft):
	"""
	Convert feet to meters
	"""
	return ft / 3.28

def reachLocation(lat, lng, alt, range, altrange):
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

def calculateStationary():
	"""
	Calculates if the drone will collide within a 2D space.
		returns x >= 0 if obstacle is within the drones flight path,
		x is the id of the obstacle

		returns -1 if no obstacle detected
	"""


def calculateEntityPath():
	"""

	"""

def drawObstacle(id, lat, lng, alt):
	"""
	Draws or redraws (updates) an obstacle on Mission Planner
	"""

def dodgeStationary(obstacleID):
	"""
	
	"""

def dodgeMotion():
	"""
	
	"""

# RUNTIME CODE

try:
	thread.start_new_thread( report_telemtry, ("Position-Thread", 0.1, ) )
except:
	print "Error: unable to start thread"



while True:
	if calculateStationary() > -1:
		# if a collision is imminent
		dodgeStationary(calculateStationary())
	else if calculateMotion() > -1:
		# if a collision is imminent
		dodgeMotion(calculateMotion())
	else:
		# if no collision is present
		time.sleep(100)


# SETUP
"""
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

"""
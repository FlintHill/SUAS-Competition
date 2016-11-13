#!/usr/local/bin/python
"""
	test drone control script
		less crashy, more fly-y

	@version	1.0
	@project	sense, detect, and avoid
	@authors	james villemarette, vale tolpegin
	@date		4-10-2016
"""
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

obstacles = []
triangles = []

r = 10
current_alt = 100

waypoint = [np.random.randint((-r)-2, r+2), 20.0]

print("Waypoint at:" + str(waypoint))

class Obstacle:
	"""
	ADD SPEED FUNCTION AND SUCH
	"""
	history = []
	lat = 0 # x
	lng = 0 # y
	alt = 0 # z 

	def __init__(self, latitude, longitude, altitude):
		self.lat = latitude
		self.lng = longitude
		self.alt = altitude

	def getLat(self): # x
		return self.lat

	def getLng(self): # y
		return self.lng

	def getAlt(self): # z
		return self.alt

class Triangle:
	"""
	Creates a triangle around an obstacle, used for calculating alternate paths.

		Triangles, in this instance, are defined as such:
				 Apex . 		-
					 / \ 		|
				(I)	/   \ (I)  	| HEIGHT
				   /     \ 		|
				  ._______. 	-
			BaseOne  (II)  BaseTwo

				  |-------|
				    BASE

			with the I, and IIs representing which side lengths are equal to each other.

		Triangles also include a rotating point at the midpoint of the base:
					  .
					 / \ 
					/   \ 
				   /     \ 
				  .___.___.		
				  [Midpoint]

			the rotating point is the where the obstacle is.
			The triangle is rotated to point towards the drone.

		These are the different points of the triangle:
			Apex    = apex
			BaseOne = b1
			BaseTwo = b2

			these variables are arrays of two floats, the indexes being:
				[0] = x
				[1] = y

		The triangle constructor can take two different types:
			Triangle(apex=[0, 2], baseOne=[-2, 1], baseTwo=[2, 1])

				which is taking in the specific points of the triangle, or

			Triangle(baseMidX=0, baseMidY=1)

				which is taking in the midpoint of the base of the triangle.

		There is also a way within the constructor to have the triangle
		point towards the origin with:
			Triangle(..., rotateToOrigin=True)
	"""
	apex = [0.0, 0.0]
	b1 = [0.0, 0.0]
	b2 = [0.0, 0.0]
	baseMid = [0.0, 0.0]

	base = 1 # 2
	height = 3 # 5

	def __init__(self, apex=None, baseOne=None, baseTwo=None, baseMid=None, rotateToOrigin=False):
		if rotateToOrigin is True:
			self.pointToOrigin()

		if apex is None and baseOne is None and baseTwo is None:
			self.apex = [baseMid[0], baseMid[1] + self.height]
			self.b1 = [baseMid[0] - self.base, baseMid[1]]
			self.b2 = [baseMid[0] + self.base, baseMid[1]]
			self.baseMid = baseMid

		if baseMid is None:
			self.apex = apex
			self.b1 = baseOne
			self.b2 = baseTwo
			self.baseMid = calculateMidpoint(baseOne[0], baseTwo[0], baseOne[1], baseTwo[2])

	def calculateMidpoint(x1, y1, x2, y2):
		"""
		Calculate the midpoint of two points
		"""
		return [(x1 + x2)/2.0, (y1 + y2)/2.0]

	def rotate(self, degrees):
		"""
		Rotate the triangle a specific amount of degrees
		"""
		r = ((-degrees) * np.pi)/180.0
		m = self.baseMid[0]
		n = self.baseMid[1]

		self.b1   = [ np.cos(r) * (self.b1[0] - m) + (self.b1[1] - n) * np.sin(r) + m, \
			-(np.sin(r)) * (self.b1[0] - m) + np.cos(r) * (self.b1[1] - n) + n ]

		self.b2   = [ np.cos(r) * (self.b2[0] - m) + (self.b2[1] - n) * np.sin(r) + m, \
			-(np.sin(r)) * (self.b2[0] - m) + np.cos(r) * (self.b2[1] - n) + n]

		self.apex = [ np.cos(r) * (self.apex[0] - m) + (self.apex[1] - n) * np.sin(r) + m, \
			-(np.sin(r)) * (self.apex[0] - m) + np.cos(r) * (self.apex[1] - n) + n]

		return True

	def angleToOrigin(self):
		"""
		If we have a line emanating from the origin going along the x-axis in
		the positive direction, what would be the angle from that line to a line
		going through the origin to the baseMid point.

		Taken from: 
			http://math.stackexchange.com/questions/1201337/finding-the-angle-between-two-points 
		"""
		return np.arctan2(self.baseMid[1], self.baseMid[0]) * 180 / np.pi

	def pointToOrigin(self):
		"""
		Have the triangle point to the origin automatically
		"""
		return self.rotate( 90 + self.angleToOrigin())

	def area(self, p1, p2, p3):
		"""
		Returns the area of a triangle with the given points:
			p1: (x1, y1), p2: (x2, y2), p3: (x3, y3)

		Taken from:
			http://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/

		Is used in pointIsOnTriangle method
		"""
		return abs((p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1]))/2.0)

	def isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0): #1e-09
		"""
		Determine if two values are in a close enough range of each other,
		rel_tol and true if they are, false if not.

		Taken from:
			https://www.python.org/dev/peps/pep-0485/#proposed-implementation

		The naming scheme on this method is different from others as it 
		represents a function that function that should be built-in
		Python which undergoes an all-lowercase naming scheme. This is
		also explained in the link above.
		"""
		return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

	def pointIsOnTriangle(self, p):
		"""
		Returns true if p point is on triangle's lines, false if not.

		Taken from:
			http://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/

		In this adaption, (where "=>" means "changed to")
			x  => p[0]
			y  => p[1]
			x1 => b1[0]
			y1 => b1[1]
			x2 => b2[0]
			y2 => b2[1]
			x3 => apex[0]
			y3 => apex[1]
		"""
		# calculate area of triangle ABC
		A = self.area([self.b1[0], self.b1[1]], [self.b2[0], self.b2[1]], [self.apex[0], self.apex[1]])

		# calculate area of triangle PBC
		A1 = self.area([p[0], p[1]], [self.b2[0], self.b2[1]], [self.apex[0], self.apex[1]])

		# calculate area of triangle PAC
		A2 = self.area([self.b1[0], self.b1[1]], [p[0], p[1]], [self.apex[0], self.apex[1]])

		# calculate area of triangle PAB
		A3 = self.area([self.b1[0], self.b1[1]], [self.b2[0], self.b2[1]], [p[0], p[1]])

		# check if sum of A1, A2 and A3 is same as A
		## using a range to determine if the result is correct because
		## most correct answers have A and (A1 + A2 + A3) off by 0.01
		## and they would be considered correct, but not evaluated as
		## such, which is the reason isclose() was implemented.
		return self.isclose(A, (A1 + A2 + A3)) #0.0005

	def isBetween(self, a, b, c):
	    crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
	    if abs(crossproduct) > 0.05 : return False   # (or != 0 if using integers)

	    dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
	    if dotproduct < 0 : return False

	    squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
	    if dotproduct > (distance(b, a)**2) : return False

	    return True

	def whatSideIsPointOn(self, p):
		"""
		Returns a string name of which side a point p lies on, 
		non-string False if not.

		The there possible responses are:
			"lengthOne",
			"lengthTwo" and,
			"base"

		If a point is on a vertex of a triangle, then this 
		function will return the vertex name which could be:
			"apex",
			"b1" and,
			"b2"

		And will just return False if the point is not on the
		triangle.

		Function works by comparing the angle of the point and
		the line by creating an additional line like so:

			|-----------| < The additional line created.
			|-----------|-----------|
			line        p           line
			Point1					Point2

			The arc tans of the two line segments are compared
			for similarity, if they're the same within a range
			of 1e-09 because certain rounding errors occur.

			A bounding box is created around the two lines so
			that just the line segments are compared, not the
			entire line.

			This bounding box is recreated in the form of
			inequality statements that are compared.
		"""
		if (p[0] == self.apex[0]) and (p[1] == self.apex[1]):
			return "apex"

		if (p[0] == self.b1[0]) and (p[1] == self.b1[1]):
			return "b1"

		if (p[0] == self.b2[0]) and (p[1] == self.b2[1]):
			return "b2"

		# 1: b1
		# 2: apex
		if self.isBetween(self.b1, self.apex, p):
			return "lengthOne"

		# 1: b2
		# 2: apex
		if self.isBetween(self.b2, self.apex, p):
			return "lengthTwo"

		# 1: b1
		# 2: b2
		if self.isBetween(self.b1, self.b2, p):
			return "base"

		return False

	def draw(self, ax):
		"""
		Draw on matplotlib
		"""
		verts = [
			(self.b1[0], self.b1[1]),     # left, bottom ||| b1 (base left)
			(self.apex[0], self.apex[1]), # left, top ||| apex (top)
			(self.b2[0], self.b2[1]),     # right, top ||| b2 (base right)
			(self.b1[0], self.b1[1]),     # ignored ||| b1 (base left)
		]
		print( "Drawing triangle with vertices: " + str(verts) )
		codes = [Path.MOVETO,
			Path.LINETO,
			Path.LINETO,
			Path.CLOSEPOLY,
		]

		path = Path(verts, codes)

		patch = patches.PathPatch(path, facecolor='orange', lw=2)
		ax.add_patch(patch)

class Line:
	"""
	Basic line definition used for storing points.

	Is a standard for using lineTriangleIntersect().
	"""
	p1 = [0.0, 0.0]
	p2 = [0.0, 0.0]

	def __init__(self, p1=None, p2=None, x1=None, y1=None, x2=None, y2=None):
		if p1 is not None and p2 is not None:
			self.p1 = p1
			self.p2 = p2
		else:
			self.p1 = [x1, y1]
			self.p2 = [x2, y2]

class ComplexLine:
	"""
	A line that contains multiple points, possibly representing a path.
	"""
	points = []

	def __init__():
		print("what")

	def draw(self, ax):
		"""
		Draw on matplotlib
		"""
		return 5

def withinVision(Obstacle):
	# disregard obstacles not in within our altitude \\
	# disregard obstacles behind us (behind the absolute function) \
	# disregard obstacles not within our scope \
	if(Obstacle.getAlt() > current_alt + 10) or \
		(Obstacle.getAlt() < current_alt - 10) or \
		((np.abs(Obstacle.getLat()) / 0.5) > np.abs(Obstacle.getLng() / 0.5)) or \
		((Obstacle.getLat() < (-r) - 2)) or ((Obstacle.getLat() > (r + 2))):
		return False

	# obstacle within our vision
	return True



def plotObstacle(ax, Obstacle_):
	ax.plot(Obstacle_.getLat(), Obstacle_.getLng(), 'ro')

def plotObstacles(ax, Obstacles_):
	i = 0
	while len(Obstacles_) > i:
		plotObstacle(ax, Obstacles_[i])
		i = i + 1

def generateObstacles(count=5):
	while len(obstacles) < count:
		x = np.random.randint(-20, 20)
		y = np.random.randint(20)

		if(withinVision(Obstacle(x, y, 100))):
			print( "Added obstacle with x:" + str(x) + " y:" + str(y))
			obstacles.append(Obstacle(x, y, 100))

def createTriangles(triangles_, obstacles_):
	"""
	Simply create triangles with the base midpoint being the obstacles position.
	"""
	for obstacle in obstacles_:
		triangles_.append(Triangle(baseMid=[obstacle.getLat(), obstacle.getLng()])) #, rotateToOrigin=True

def drawTriangles(triangles_, ax):
	for triangle in triangles_:
		triangle.draw(ax)

# functions critical to avoidance

def distance(p1, p2):
	"""
	Calculate the distance between two points.
	"""
	#if 
	return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def lineIntersect(x1, y1, x2, y2, x3, y3, x4, y4):
	"""
	Returns a point if two lines intersect.

	False if not.

	Inspired by: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
	"""
	### DEBUG:
	print( str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(x3) + " " + str(y3) + " " + str(x4) + " " + str(y4) )

	if ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)) == 0:
		return False

	result = [ \
		(( ((x1*y2) - (y1*x2))*(x3 - x4) - (x1 - x2)*((x3*y4) - (y3*x4)) ) / \
		( (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4) )), \
		(((x1*y2) - (y1*x2))*(y3 - y4) - (y1 - y2)*((x3*y4) - (y3*x4))) / \
		((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)) \
		]

	someCrazyNumber = 7205759403792796.0 - 1

	if result[0] > someCrazyNumber and result[1] > someCrazyNumber:
		return False

	return result

def lineIntersectCompact(p1, p2, p3, p4):
	"""
	lineIntersect() with minified inputs. Takes in four inputs which are 
	four points.

	Points are lists with x in [0] and y in [1].

	Returns the same result as lineIntersect(), a point if the two lines
	intersect, false if not.
	"""
	return lineIntersect(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1])

def lineTriangleIntersect(line, triangle):
	"""
	2D:
		Returns true if a line intersects a triangle, false if not.

	Line variable requires Line class which has the basic structure of:
		p1 = [0.0, 0.0]
		p2 = [0.0, 0.0]

		(example values filled in)
	"""
	# intersection with line and triangle: b1 to apex
	result = lineIntersectCompact(line.p1, line.p2, triangle.b1, triangle.apex)

	if result is not False:
		return result

	result = lineIntersectCompact(line.p1, line.p2, triangle.b2, triangle.apex)

	if result is not False:
		return result

	result = lineIntersectCompact(line.p1, line.p2, triangle.b1, triangle.b2)

	if result is not False:
		return result

	return False

def firstIntersection(ray, triangle):
	"""
	2D:
		Calculates and returns a list with:
			[0-1]:
				First intersection as x [0] and y [1]
			[2]:
				String of triangle side intersected: "base", "lengthOne", or "lengthTwo"

		This graphic depicting which sides are which is reiterated 
		from Triangle class definition:

						  .
						 / \ 
			lengthOne	/   \	lengthTwo
					   /     \ 
					  ._______.	
					  	base

		Important: The point of first intersection returned, assuming if a 
		point of intersection exists, will be the first point in the ray 
		and the point on the triangle that is closest.
	"""
	results = []
	results.append( lineIntersectCompact(ray.p1, ray.p2, triangle.b1, triangle.apex) )
	results.append( lineIntersectCompact(ray.p1, ray.p2, triangle.b2, triangle.apex) )
	results.append( lineIntersectCompact(ray.p1, ray.p2, triangle.b1, triangle.b2) )

	# check if there's any intersection to begin with
	allFalse = True

	for result in results:
		if result is not False:
			allFalse = False

	if allFalse:
		return False # no intersection, don't waste comp power or time

	# any results that do not intersect are given -1 as to be pushed to bottom in sorting
	# give results distances
	compiled = []
	origin   = [0.0, 0.0]

	for result in results:
		if result is not False and triangle.pointIsOnTriangle(result) is True:
			compiled.append((result, distance(origin, result)))

	# sort and return results from least to greatest distance
	return sorted(compiled, key=lambda result:result[1])

def intersectWithinObstacles(ray, triangles):
	for x-axis	
		intersect()

# avoidance part

def shortestRouteAvoidance(triangles_, draw=False, ax=None):
	"""
	Starts from the drones current position, then looks at all the available points
	(triangle points) and looks for the closest point, then if no more obstacles
	lie on the x-axis or the path to the waypoint, continue forward.
	"""
	path = []

	apex_points = []
	b1_points   = []
	b2_points   = []

	# compile points
	for triangle in triangles:
		apex_points.append(triangle.apex)
		b1_points.append(triangle.b1)
		b2_points.append(triangle.b2)

	# begin searching
	#i = 0
	"""
	for 
		shortestPoint = None

		for point in apex_points:
			if distance(point) < distance(shortestPoint)
	"""
	x


#obstacles.append(Obstacle(0, 5, 100))
#triangles.append(Triangle(baseMid=[0.0, 5.0]))
#print(withinVision(obstacles[0]))

# declare
fig, ax = plt.subplots()

# test
generateObstacles()
plotObstacles(ax, obstacles)
createTriangles(triangles, obstacles)

for triangle in triangles:
	print( str(triangle.pointToOrigin()) )

drawTriangles(triangles, ax)
#triangles[0].draw(ax)

# details
ax.set_xlim(-30, 30)
plt.xlabel('west to east (m)')
plt.ylabel('north to south (m)')
plt.title('Sense, Detect, and Avoid: Obstacle Avoidance (Demo)')

# add in safety_radius and scope
circle1 = plt.Circle((0, 0), r, color='r', zorder=-1, alpha=0.2, label='safety radius')
circleWaypoint = plt.Circle((waypoint[0], waypoint[1]), 1, color='y', zorder=-1, label='waypoint')
ax.add_artist(circle1)
ax.add_artist(circleWaypoint)

# add in direction of the drone from origin to waypoint
ax.plot([0, waypoint[0]], [0, waypoint[1]], 'ro', linestyle='dotted', label='direct trajectory')

# plot scope
ax.plot([-(r) - 1, 0, r + 1],[(r/2), 0, (r/2)], color='blue', label='scope') # absolute function
ax.plot([-1 - r, -1 - r], [20, -20], color='blue') # left inequality
ax.plot([1 + r, 1 + r], [20, -20], color='blue') # right inequality

# visualize betterer (fix aspect ratio and figure size)
plt.rcParams["figure.figsize"] = [20, 20]
ax.set_aspect('equal')
ax.grid(True, which='both')

plt.legend()

# x and y-axis visible
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')

# plot drone
plt.plot([0], [0], "ro")

# update onclick
#def clearArrays():
#	del obstacles[:]
#	del triangles[:]

"""
def onclick(event):
	clearArrays()
	generateObstacles()
	plotObstacles(ax, obstacles)
	createTriangles(triangles, obstacles)

	for triangle in triangles:
		print( str(triangle.pointToOrigin()) )

	drawTriangles(triangles, ax)

	# Refresh the plot
	fig.canvas.draw()
"""

#cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
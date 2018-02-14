import sys
from os import walk
import cv2
import numpy as np

from .logger import Logger
from .settings import ImageProcessingClassifierSettings

from PIL import Image

class ColorClassifier(object):
	"""
	Step 4: Autonomously classify shape color and alphanumeric color.
	"""

	def __init__(self, img=None):
		"""
		Constructor.

		:param img:		Relative path to image.
		:type img:		String

		:return:		Nothing.
		"""
		self.img = img

	def get_color(self):
		"""
		Gets the color of the background and text inside a target.

		If no img is passed to get_color, then this function assumes to use the
		PIL image passed in the constructor.

		See section 3 for code source:
			https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/
			py_kmeans_opencv/py_kmeans_opencv.html

		:return:		Two element list, where the first element is the shape
						color, and the second element is the text color. Ex:
							["red", "green"]
						or, simply:
							[<background color>, <text color>]
		"""
		if self.img is None:
			raise Exception("classify_color.py: No image was passed in the constructor.")

		opened_img = Image.open(self.img)
		lines_to_grab = 6

		Logger.log("classify_color.py: Starting work on new image.")

		# convert pil to opencv2
		img = np.array(opened_img)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		Z = img.reshape((-1,3))

		# convert to np.float32
		Z = np.float32(Z)

		# define criteria, number of clusters(K) and apply kmeans()
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		K = 3
		ret,label,center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

		# now convert back into uint8, and make original image
		center = np.uint8(center)
		flattened_img = center[label.flatten()]
		reshaped_img = flattened_img.reshape((img.shape))

		# grab colors
		corrected_img = cv2.cvtColor(reshaped_img, cv2.COLOR_RGB2BGR)
		colors_from_img = set(tuple(v) for m2d in corrected_img for v in m2d)

		Logger.log("classify_color.py: Raw colors from image: " + str(colors_from_img))

		color_names_from_img = []

		for pixel_from_img in colors_from_img:
			color_names_from_img.append(self.convert_rgba_to_color_name(list(pixel_from_img)))

		if "white" in color_names_from_img:
			color_names_from_img.remove("white") # remove background

		# figure out which color comes first, reading from the center row outwards
		height, width, channels = img.shape
		row_factor = int(round(height/(float(lines_to_grab) + 1.0)))

		shape_color = None
		text_color = None
		row = 0

		im = opened_img
		im_width, im_height = im.size
		pixels = list(im.getdata())

		count = {
			colors_from_img.pop(): 0,
			colors_from_img.pop(): 0,
			colors_from_img.pop(): 0
		}

		Logger.log("classify_color.py: Count before: ")
		Logger.log("classify_color.py: " + str(count))

		for line in range(lines_to_grab):
			row = row + row_factor

			Logger.log("classify_color.py: Line collection #" + str(line + 1) + " start at height: " + str(row))

			for column in range(1, width):
				# check original image to see if alpha is 0
				if pixels[(im_width * row) + column] == (255, 255, 255, 0):
					pass # empty, transparent background pixel
				else:
					count[tuple(corrected_img.tolist()[row][column])] += 1


		Logger.log("classify_color.py: Count results: ")
		Logger.log("classify_color.py: " + str(count))

		new_count = {}

		for i in range(len(count.keys())):
			new_count[self.convert_rgba_to_color_name(list(count.keys()[i]))] = count[count.keys()[i]]

			Logger.log("classify_color.py: Discovered color: " + str(list(count.keys()[i])) + " as " + self.convert_rgba_to_color_name(list(count.keys()[i])))

		Logger.log("classify_color.py: Count color rgb convert to names: ")
		Logger.log("classify_color.py: " + str(new_count))

		# determine shape and content color based on max and min
		maximum = 0
		minimum = 0

		if len(new_count.keys()) == 3:
			maximum = max(new_count, key=new_count.get)

			del new_count[min(new_count, key=new_count.get)]

			minimum = min(new_count, key=new_count.get)
		else: # if background color is white
			if new_count[new_count.keys()[0]] >= new_count[new_count.keys()[1]]:
				maximum = new_count.keys()[0]
				minimum = new_count.keys()[1]
			else:
				maximum = new_count.keys()[1]
				minimum = new_count.keys()[0]

		Logger.log("classify_color.py: Determined shape color to be '" + maximum + "'")
		Logger.log("classify_color.py: Determined text color to be '" + minimum + "'")

		result = [maximum, minimum]

		return result

	def three_dimesional_distance(self, p1, p2):
		"""
		Calculates the distance between two three dimesional points.

		p1 or p2 should be a list of three elements:
			[x, y, z]

		:param p1:	point one with x, y, z.
		:param p2:	point two with x, y, z.

		:type p1:	three element list.
		:type p2:	three element list.

		:return:	float distance.

		See page 3 of:
			http://www.math.usm.edu/lambers/mat169/fall09/lecture17.pdf
		"""
		return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)

	def convert_rgba_to_color_name(self, rgba):
		"""
		Using min-distance approximation, this function converts the rgba value,
		which is a list of [r, g, b, a] into it's closest color name, which are
		as follows:

			"white": [255, 255, 255, 255]
			"black": [0, 0, 0, 255]
			"gray": [128, 128, 128, 255]
			"red": [255, 0, 0, 255]
			"blue": [0, 0, 255, 255]
			"green": [0, 255, 0, 255]
			"yellow": [255, 255, 0, 255]
			"purple": [128, 0, 128, 255]
			"brown": [165, 42, 42, 255]
			"orange": [255, 165, 0, 255]

		:param rgba:	color component in the format [r, g, b, a].
		:type rgba:		four element list.

		:return:		"white", "black", etc.
		"""

		distances = []
		i = 0

		for color in ImageProcessingClassifierSettings.COLORS.keys():
			distances.append(0)

			c = ImageProcessingClassifierSettings.COLORS[color]

			distances[i] = self.three_dimesional_distance(
				[rgba[0], rgba[1], rgba[2]],
				[c[0], c[1], c[2]]
			)

			i += 1

		# approximate color name based on min-distance
		d = sys.maxint
		i = 0
		j = 0

		for distance in distances:
			if distance < d:
				d = distance
				i = j

			j += 1

		return ImageProcessingClassifierSettings.COLORS.keys()[i]

	def convert_color_name_to_rgba(self, color_name):
		"""
		Takes in a cardinal color name and converts it to an rgba value with
		100 percent alpha.

		:param color_name:	Cardinal name of color.

							Either "white", "black",
							"gray", "red", "blue", "green", "yellow", "purple",
							"brown", or "orange".

		:type color_name:	String.

		:return:			rgba version of color.
		"""
		return ImageProcessingClassifierSettings.COLORS[color_name]

import sys
from os import walk
import cv2
import numpy as np

#from ..settings import ImgProcSettings

from PIL import Image

class ColorClassifier(object):
	"""
	Step 4: Autonomously classify shape color and alphanumeric color.
	"""

	def __init__(self, img=None):
		"""
		Constructor.

		:param img:		Opened PIL (Python Image Library) image.
		:type img:		PIL.Image.Image

		:return:		Nothing.
		"""
		self.img = img

		self.colors = {
			"white": [255, 255, 255, 255],
			"black": [0, 0, 0, 255],
			"gray": [128, 128, 128, 255],
			"red": [255, 0, 0, 255],
			"blue": [0, 0, 255, 255],
			"green": [0, 255, 0, 255],
			"yellow": [255, 255, 0, 255],
			"purple": [128, 0, 128, 255],
			"brown": [165, 42, 42, 255],
			"orange": [255, 165, 0, 255]
		}

	#@staticmethod
	def get_color(self, img=None):
		"""
		Gets the color of the background and text inside a target.

		If no img is passed to get_color, then this function assumes to use the 
		PIL image passed in the constructor.

		See section 3 for code source:
			https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/
			py_kmeans_opencv/py_kmeans_opencv.html

		:param img:		optional. An opened PIL image.
		:type img:		PIL object.

		:return:		Two element list, where the first element is the shape
						color, and the second element is the text color. Ex:
							["red", "green"]
						or, simply:
							[<background color>, <text color>]
		"""
		opened_img = Image.open(self.img)

		# convert pil to opencv2
		img = np.array(opened_img)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		Z = img.reshape((-1, 3))

		# convert to np.float32
		Z = np.float32(Z)

		# define criteria, number of clusters(K) and apply kmeans()
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		K = 3
		ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

		# now convert back into uint8, and make original image
		center = np.uint8(center)
		res = center[label.flatten()]
		res2 = res.reshape((img.shape)) # actual image

		# grab colors from image
		res3 = cv2.cvtColor(res2, cv2.COLOR_RGB2BGR)
		colors_from_img = set( tuple(v) for m2d in res3 for v in m2d )

		print("classify_color.py: Raw colors from image: " + str(colors_from_img))

		color_names_from_img = []
		for pixel_from_img in colors_from_img:
			color_names_from_img.append(self.convert_rgba_to_color_name(list(pixel_from_img)))

		if "white" in color_names_from_img:
			color_names_from_img.remove("white") # remove background

		print("classify_color.py: Converted color names: " + str(color_names_from_img))

		# figure out which color comes first, reading from the center row outwards
		height, width, channels = img.shape
		print("classify_color.py: Height of image is " + str(height) + "px and width is " + str(width) + "px.")
		print("classify_color.py: Height divided by 2, rounded, is " + str(int(round(height/2.0))) + ".")

		row = int(round(height/2.0))

		shape_color = None
		text_color = None

		for column in range(1, width):
			if self.convert_color_name_to_rgba(self.convert_rgba_to_color_name(res3[row, column])) == self.convert_color_name_to_rgba(color_names_from_img[0]):
				shape_color = color_names_from_img[0]
				text_color = color_names_from_img[1]
			elif self.convert_color_name_to_rgba(self.convert_rgba_to_color_name(res3[row, column])) == self.convert_color_name_to_rgba(color_names_from_img[1]):
				shape_color = color_names_from_img[1]
				text_color = color_names_from_img[0]

			if shape_color != None and text_color != None:
				print("classify_color.py: Determined shape color to be " + str(shape_color) + ".")
				print("classify_color.py: Determined text color to be " + str(text_color) + ".")
				break;

		result = [shape_color, text_color]

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

		for color in self.colors.keys():
			distances.append(0)

			c = self.colors[color]

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

		return self.colors.keys()[i]


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
		return self.colors[color_name]

	def __str__(self):
		"""
		To string method.

		:return:	Nothing.
		"""
		print("<COLOR CLASSIFIER>")
		print("Type:     Object.")
		print("")
		print("</COLOR CLASSIFIER>")

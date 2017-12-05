import sys
from os import walk
#import cv2
import numpy as np

try:
	from PIL import Image
except ImportError:
	import Image


class ColorClassifier(object):
	"""
	Step 4: Autonomously classify shape color and alphanumeric color.
	"""

	def __init__(self, img=None, imgs=None):
		"""
		Constructor. 
		"""
		if img is not None and imgs is not None:
			raise Exception("classify_color.py: Cannot pass both an img object and imgs array")

		self.imgs = []
		self.results = []
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

		if img is not None:
			self.imgs.append(img)
		elif imgs is not None:
			self.imgs = imgs

	def load_images(self, image_dir, count=sys.maxint):
		"""
		Import all (or a specific number of) the target images from a specified 
		directory.

		:param image_dir:	target images dir. ex: "targets/single_targets"
		:param count:		number of images to load, starting from the lowest
							file name ascending.

							ex: 
							when count=3:
							["1.jpg", "2.jpg", "3.jpg"]
		"""
		for (dirpath, dirnames, filenames) in walk(image_dir):
			self.imgs = filenames
			break

		self.imgs.sort(key=lambda f: int(filter(str.isdigit, f)))

		self.imgs = np.array(self.imgs)

		if count != sys.maxint:
			self.imgs = self.imgs[0:count]

	def add_images(self, new_imgs):
		"""

		"""

	def get_color(self, img):
		"""

		"""
		# collect unique colors and number how many there are

		# check colors in center

		# compare against unique color list

		# report shape color background only

		return True

	def get_colors(self, verbose=False):
		"""
		If ColorClassifier has been passed the filenames of multiple images,
		then 
		"""
		if len(self.imgs) == 1:
			return get_color(self.imgs[0])

		output = []

		for img in self.imgs:
			output.append(self.get_color(img))

		return output

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
		print("----- COLOR CLASSIFIER -----")
		print("Type:     Object.")
		print("Contains: " + str(len(imgs)) + " images.")
		print("Files:")
		print("")

		self.print_image_filenames()

		print("")
		print("----- END COLOR CLASSIFIER -----")




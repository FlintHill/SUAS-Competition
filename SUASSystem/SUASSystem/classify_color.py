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
		Constructor
		"""
		if img is not None and imgs is not None:
			raise Exception("classify_color.py: Cannot pass both an img object and imgs array")

		self.imgs = []
		self.results = []

		if img is not None:
			self.imgs.append(img)
		elif imgs is not None:
			self.imgs = imgs

	def load_images(self, image_dir, count=sys.maxint):
		"""
		Import all the targets images from a specified directory.

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

	def get_color():
		return True

	def get_colors(self, verbose=False):
		"""

		"""
		for img in self.imgs:
			self.results.append("[192, 192, 192, 255]")

		# collect unique colors and number how many there are

		# check colors in center

		# compare against unique color list

		# report shape color background only

		return self.results

	def convert_rgb_to_color_name(rgba):
		# approximate color name based on min-distance
		return [0, 255, 255, 255]

	def convert_color_name_to_rgb(color_name):
		"""
		Takes in a cardinal color name and converts it to an rgba value with
		100 percent alpha.
		"""
		return {
			"red": 
		}[color_name]

	def __str__(self):
		print("----- COLOR CLASSIFIER -----")
		print("Type:     Object.")
		print("Contains: " + str(len(imgs)) + " images.")
		print("Files:")
		print("")

		self.print_image_filenames()

		print("")
		print("----- END COLOR CLASSIFIER -----")




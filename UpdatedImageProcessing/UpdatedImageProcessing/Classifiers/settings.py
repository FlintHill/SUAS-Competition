class ImageProcessingClassifierSettings(object):
	"""
	Settings used across all classifiers.
	"""

	LOGGING_ON = False

	COLORS = {
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

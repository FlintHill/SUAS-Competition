try:
	from PIL import Image
except ImportError:
	import Image

import sys
import numpy as np
import cv2

colors = {
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

def three_dimesional_distance(p1, p2):
	return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)

def convert_rgba_to_color_name(rgba):
	distances = []
	i = 0	

	for color in colors.keys():
		distances.append(0)

		c = colors[color]

		distances[i] = three_dimesional_distance(
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

	return colors.keys()[i]

passed = Image.open('targets_new/single_targets/1.png').convert('RGB')

# convert pil to opencv2
img = np.array( passed  ) 
img = img[:, :, ::-1].copy() # convert rgb to bgr 

Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret,label,center=cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape)) # actual image

# grab colors from image
colors_from_img = set( tuple(v) for m2d in res2 for v in m2d )

color_names_from_img = []

for color in colors_from_img:
	color_names_from_img.append(convert_rgba_to_color_name(list(color)))

print(color_names_from_img)

# figure out which color comes first, reading from the center row outwards

# shows image
cv2.imshow('res2',res2)
cv2.waitKey(0)
cv2.destroyAllWindows()


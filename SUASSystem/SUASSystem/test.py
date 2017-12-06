
"""import sys

a = [1, 2, 3]
b = [4, 5, 6]



print( [x + y for x, y in zip(a, b)] )

sys.exit()"""

import sys
import numpy as np

try:
	from PIL import Image
except ImportError:
	import Image

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

#fault_tolerance = 40 # 3d distance of a pixel before its considered a new color

im = Image.open('targets_new/single_targets/1.png')

pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]




#print(pixels[0][0])
#print(pixels[0][0] == (255, 255, 255, 0))
#sys.exit()



#count = []
#color = []



#print pixels


"""
for row in pixels:
	for pixel in row:
		#print(str(pixel[0]) + " ?= (255, 255, 255, 0)" )
		if pixel != (255, 255, 255, 0): # ignore background
			if len(color) == 0:
				count.append(1)
				color.append(list(pixel))
			else:
				print(convert_rgba_to_color_name(list(pixel)))

				j = 0
				dist = 0
				pos = 0

				#print color

				for c in color:
					#print(pixel[0][0])

					distance = three_dimesional_distance(
						[pixel[0], pixel[1], pixel[2]],
						[c[0], c[1], c[2]]
					)

					if distance < dist:
						dist = distance
						pos = j

					if len(color) > 1:
						j += 1

				if dist > fault_tolerance:
					count.append(1)
					color.append(list(pixel))
				else:
					count[j] += 1
					color[j] = [x + y for x, y in zip(color[j], pixel)]
		#else:
		#	#print("bounce")


for i, s in enumerate(color[0]):
	color[0][i] = s / count[0]

print count
print color
print( "count len: " + str(len(count)) )
print( "color len: " + str(len(color)) )
print(convert_rgba_to_color_name(color[0]))
print str(len(pixels))
"""
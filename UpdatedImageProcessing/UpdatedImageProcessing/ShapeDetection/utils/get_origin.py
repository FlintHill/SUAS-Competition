import numpy
from PIL import Image

def get_origin(canny_img):
    image = canny_img.load()
    pixels_x = []
    pixels_y = []
    for x in range(0, canny_img.size[0]):
        for y in range(0, canny_img.size[1]):
            if image[x,y] != 0:
                pixels_x.append(x)
                pixels_y.append(y)
    pixels_x = numpy.asarray(pixels_x)
    pixels_y = numpy.asarray(pixels_y)
    x_mean = int(numpy.mean(pixels_x))
    y_mean = int(numpy.mean(pixels_y))

    return(x_mean, y_mean)

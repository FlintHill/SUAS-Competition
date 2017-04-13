import numpy

def get_color_histogram(img, image, bin_size = 1):
    histogram = numpy.zeros((255,255,255))

    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            pixel_color = image[x,y]
            start_indexes = (pixel_color[0]//bin_size, pixel_color[1]//bin_size, pixel_color[2]//bin_size)
            for r in range(start_indexes[0], start_indexes[0]+bin_size):
                for g in range(start_indexes[1], start_indexes[1]+bin_size):
                    for b in range(start_indexes[2], start_indexes[2]+bin_size):
                        histogram[r,g,b] += 1
    return histogram

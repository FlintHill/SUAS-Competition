import numpy


def get_bw_img_mean_pixel(img, image):
    pixels_x = []
    pixels_y = []
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            if image[x,y] != 0:
                pixels_x.append(x)
                pixels_y.append(y)
    pixels_x = numpy.asarray(pixels_x)
    pixels_y = numpy.asarray(pixels_y)
    x_mean = int(numpy.mean(pixels_x))
    y_mean = int(numpy.mean(pixels_y))
    return(x_mean, y_mean)

def get_mean_color_excluding_transparent(img, image):
    sums = [0,0,0]
    num_pixels = 0
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            if image[x,y][3] != 0:
                num_pixels += 1
                for i in range(0, 3):
                    sums[i] += image[x,y][i]
    if num_pixels == 0:
        return (0,0,0)
    for i in range(0, len(sums)):
        sums[i]/=float(num_pixels)  
    return tuple(sums)       
    
                
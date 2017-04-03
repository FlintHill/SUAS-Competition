import numpy
from PIL import Image, ImageDraw

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

def merge_channels(dim, channel_images):
    out_img = Image.new("RGB", dim)
    out_image = out_img.load()
    for x in range(0, dim[0]):
        for y in range(0, dim[1]):
            out_image[x,y] = (channel_images[0][x,y], channel_images[1][x,y], channel_images[2][x,y])
    return out_img

def get_binary_bw_img(img, image, threshold):
    out_img = Image.new('L', img.size)
    out_image = out_img.load()
    for x in range(0, out_img.size[0]):
        for y in range(0, out_img.size[1]):
            out_image[x,y] = 255 if image[x,y] >= threshold else 0
    return out_img

'''will crash if the images have different types. Often images will be loaded as RGBA instead of just RGB. To fix this,
use Image.convert('RGB') before passing'''
def subtract(dim, base_image, sub_image):
    out_arr = numpy.zeros(dim, dtype = tuple)
    for x in range(0, dim[0]):
        for y in range(0, dim[1]):
            out_arr[x,y] = tuple(numpy.subtract(tuple(base_image[x,y]), tuple(sub_image[x,y])))
    return out_arr

def get_bw_connected_components_map(img, image):
    fill_mask = img.copy()
    fill_image = fill_mask.load()
    connected_components_map = numpy.zeros(fill_mask.size, dtype = int)
    component_number = 1
    for x in range(0, fill_mask.size[0]):
        for y in range(0, fill_mask.size[1]):
            if fill_image[x,y] == 255:
                ImageDraw.floodfill(fill_mask, (x,y), 128)

                for i in range(0, connected_components_map.shape[0]):
                    for j in range(0, connected_components_map.shape[1]):
                        if fill_image[i,j] == 128:
                            connected_components_map[i,j] = component_number
                            fill_image[i,j] = 0
                component_number += 1
    return connected_components_map

def convert_connected_component_map_into_clusters(connected_components_map):
    num_connected_components = numpy.amax(connected_components_map)
    connected_component_pixels = [[] for i in range(0, num_connected_components)]
    for x in range(0, connected_components_map.shape[0]):
        for y in range(0, connected_components_map.shape[1]):
            if connected_components_map[x,y] != 0:
                connected_component_pixels[int(connected_components_map[x,y]-1)].append((x,y))
    return connected_component_pixels

def get_connected_component_mask(dim, connected_component):
    out_img = Image.new('L', dim)
    out_image = out_img.load()
    for i in range(0, len(connected_component)):
        out_image[connected_component[i][0], connected_component[i][1]] = 255
    return out_img

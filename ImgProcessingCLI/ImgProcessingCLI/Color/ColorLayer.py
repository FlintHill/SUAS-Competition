from PIL import Image
from ImgProcessingCLI.ImageOperation import *
import numpy

class ColorLayer(object):

    def __init__(self, color_in, dim_in):
        self.color = color_in
        self.layer_img = Image.new('L', dim_in, 0)
        self.layer_image = self.layer_img.load()
        self.area = 0
        self.init_bounds()

    def paint_pixel(self, pixel):
        self.layer_image[pixel[0], pixel[1]] = 255
        self.area += 1

    '''takes a picture of the same dimensions as this color layer. Fills in the dark areas of this color layer
    if the input color layer is white there'''
    def fill_with_color_layer(self, color_layer_in):
        for x in range(0, self.layer_img.size[0]):
            for y in range(0, self.layer_img.size[1]):
                if color_layer_in.get_layer_image()[x,y] != 0:
                    self.layer_image[x,y] = 255

    def get_layer_filled_with_layer(self, color_layer_in):
        layer_clone = self.clone()
        layer_clone.fill_with_color_layer(color_layer_in)
        return layer_clone


    def init_bounds(self):
        self.bounds = get_bw_img_bounds(self.layer_img, self.layer_image)

    def get_bounds(self):
        return self.bounds

    def get_area(self):
        return self.area

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_layer_img(self):
        return self.layer_img

    def set_layer_img(self, img_in):
        self.layer_img = img_in
        self.layer_image = self.layer_img.load()
        self.init_bounds()
        self.init_area()

    def init_area(self):
        self.area = 0
        for x in range(0, self.layer_img.size[0]):
            for y in range(0, self.layer_img.size[1]):
                if self.layer_image[x,y] != 0:
                    self.area += 1
        #needs to recalculate area!

    def get_layer_image(self):
        return self.layer_image

    def get_avg_dist_from_center(self):
        sum_num = 0
        num_counted = 0
        center = numpy.array([self.layer_img.size[0]/2, self.layer_img.size[1]/2])
        for x in range(0, self.layer_img.size[0]):
            for y in range(0, self.layer_img.size[1]):
                if self.layer_image[x,y] != 0:
                    pixel = numpy.array([x-center[0], y - center[1]])
                    sum_num += numpy.linalg.norm(pixel)
                    num_counted += 1
        return sum_num/float(num_counted)

    def clone(self):
        clone_layer = ColorLayer(self.color, self.layer_img.size)
        clone_layer.set_layer_img(self.layer_img.copy())
        return clone_layer

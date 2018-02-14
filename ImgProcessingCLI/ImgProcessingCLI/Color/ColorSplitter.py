from ImgProcessingCLI.Color import *
from ImgProcessingCLI.Array import ArrayHelper
from ImgProcessingCLI.ImgStat import KMeans
import time
import numpy

class ColorSplitter(object):

    def __init__(self, img_in, image_in):
        self.img = img_in
        self.image = image_in
        self.color_layers = ColorLayers()
        self.init_color_layers()
        self.split_colors()

    @classmethod
    def init_with_kmeans(cls, img_in, image_in, num_clusters_in, times_to_run, step=1):
        kmeans = KMeans.init_with_img(img_in, image_in, num_clusters_in, times_to_run, step)
        kmeans_colors = kmeans.get_cluster_origins_int()
        kmeans_img = ColorMath.get_img_rounded_to_colors(img_in, image_in, kmeans_colors)
        kmeans_image = kmeans_img.load()
        kmeans_img.show()
        return ColorSplitter(kmeans_img, kmeans_image)

    def init_color_layers(self):
        for x in range(0, self.img.size[0]):
            for y in range(0, self.img.size[1]):
                if (ArrayHelper.search(self.color_layers, self.image[x,y], key=lambda layer: layer.get_color()) == None):
                    self.color_layers.append_color_layer(ColorLayer(self.image[x,y], self.img.size))

    def split_colors(self):
        for x in range(0, self.img.size[0]):
            for y in range(0, self.img.size[1]):
                color_index = ArrayHelper.search(self.color_layers, self.image[x,y], key = lambda layer: layer.get_color())
                self.color_layers[color_index].paint_pixel((x,y))

    def sort_by_area(self):
        self.color_layers.set_color_layers( sorted(self.color_layers, key=lambda layer: layer.get_area()))

    def get_layers_sorted_by_avg_dist_to_center(self):
        return sorted(self.color_layers, key=lambda layer: layer.get_avg_dist_from_center())

    '''sorting by area is a simple (not sure if always effective, needs testing) way to layer the image from
    front to back, allowing you to fill holes of layers beneath other layers'''
    def sort_then_fill_gaps(self, sort_function):
        sort_function()
        for i in range(0, len(self.color_layers) - 1):
            self.color_layers[i+1].fill_with_color_layer(self.color_layers[i])

    def get_color_layers(self):
        return self.color_layers

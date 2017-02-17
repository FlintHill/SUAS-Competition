from Color.ColorLayers import ColorLayers
from Color.ColorLayer import ColorLayer
import Array.ArrayHelper as ArrayHelper
import time

class ColorSplitter:
    def __init__(self, img_in, image_in):
        self.img = img_in
        self.image = image_in
        self.color_layers = ColorLayers()
        self.init_color_layers()
        self.split_colors()
        self.sort_by_area_then_fill_gaps()
        
    def init_color_layers(self):
        for x in range(0, self.img.size[0]):
            for y in range(0, self.img.size[1]):    
                if (ArrayHelper.search(self.color_layers, self.image[x,y], key=lambda layer: layer.get_color()) == None):
                    print("color layer added")
                    self.color_layers.append_color_layer(ColorLayer(self.image[x,y], self.img.size))
        
    def split_colors(self):
        for x in range(0, self.img.size[0]):
            for y in range(0, self.img.size[1]):
                color_index = ArrayHelper.search(self.color_layers, self.image[x,y], key = lambda layer: layer.get_color())
                self.color_layers[color_index].paint_pixel((x,y))    
    
    def sort_by_area(self):
        self.color_layers = sorted(self.color_layers, key=lambda layer: layer.get_area())
    '''sorting by area is a simple (not sure if always effective, needs testing) way to layer the image from
    front to back, allowing you to fill holes of layers beneath other layers'''
    def sort_by_area_then_fill_gaps(self):
        self.sort_by_area()
        for i in range(0, len(self.color_layers) - 1):
            self.color_layers[i+1].fill_with_color_layer(self.color_layers[i])
    
    def get_color_layers(self):
        return self.color_layers
                
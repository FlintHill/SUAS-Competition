from PIL import Image
import ImageOperation.Crop as Crop

class ColorLayer:
    
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
                if self.layer_image[x,y] != 255 and color_layer_in.get_layer_image()[x,y] == 255:
                    self.layer_image[x,y] = 255
    
    def init_bounds(self):
        self.bounds = Crop.get_bw_img_bounds(self.layer_img, self.layer_image)    
    
    def get_area(self):
        return self.area
    
    def get_color(self):
        return self.color
    
    def get_layer_img(self):
        return self.layer_img
    
    def get_layer_image(self):
        return self.layer_image
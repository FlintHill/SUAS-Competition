

class Rectangle:
    
    def __init__(self, x_in, y_in, width_in, height_in):
        self.x = x_in
        self.y = y_in
        self.width = width_in
        self.height = height_in
        
    def fill(self, img, image, color):
        for x in range(self.x, self.x+self.width):
            for y in range(self.y, self.y+self.height):
                if x > 0 and x < img.size[0] and y > 0 and y < img.size[1]:
                    image[x,y] = color
        return None       
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
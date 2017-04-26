import numpy

class Rectangle(object):

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

    def draw(self, img, image, color):
        for x in range(self.x, self.x+self.width):
            if x > 0 and x < img.size[0]:
                if self.y > 0 and self.y < img.size[1]:
                    image[x,self.y] = color
                if self.y + self.height > 0 and self.y + self.height < img.size[1]:
                    image[x,self.y+self.height] = color
        for y in range(self.y, self.y+self.height):
            if y > 0 and y < img.size[1]:
                if self.x > 0 and self.x < img.size[0]:
                    image[self.x, y] = color
                if self.x > 0 and self.x + self.width < img.size[0]:
                    image[self.x+self.width, y] = color

    def as_points(self):
        return numpy.array([[self.x, self.y],
                            [self.x+self.width, self.y],
                            [self.x+self.width, self.y+self.height],
                            [self.x, self.y+self.height]])

    def get_avg_distance_to_points(self, point):
        points = self.as_points()
        sum = 0
        for i in range(0, points.shape[0]):
            sum += numpy.linalg.norm(numpy.subtract(point, points[i]))
        return sum/float(points.shape[0])

    def get_if_rect_overlaps(self, compare_rect):
        return (self.x <= compare_rect.get_x() + compare_rect.get_width() and self.x + self.width >= compare_rect.get_x() and self.y <= compare_rect.get_y() + compare_rect.get_height() and self.y + self.height >= compare_rect.get_y())

    @staticmethod
    def get_bounding_box_of_rectangles(rects):
        left = rects[0].get_x()
        right = rects[0].get_x() + rects[0].get_width()
        top = rects[0].get_y()
        bottom = rects[0].get_y() + rects[0].get_height()
        for i in range(1, len(rects)):
            iter_left = rects[i].get_x()
            iter_right = iter_left + rects[i].get_width()
            iter_top = rects[i].get_y()
            iter_bottom = iter_top + rects[i].get_height()
            if iter_left < left:
                left = iter_left
            if iter_right > right:
                right = iter_right
            if iter_top < top:
                top = iter_top
            if iter_bottom > bottom:
                bottom = iter_bottom
        return Rectangle(left, top, right - left, bottom - top)

    def get_x(self):
        return self.x

    def set_x(self, x_in):
        self.x = x_in

    def get_y(self):
        return self.y

    def set_y(self, y_in):
        self.y = y_in

    def get_width(self):
        return self.width

    def get_center(self):
        return numpy.array([self.x + self.width//2, self.y + self.height//2])

    def set_width(self, width_in):
        self.width = width_in

    def get_height(self):
        return self.height

    def set_height(self, height_in):
        self.height = height_in

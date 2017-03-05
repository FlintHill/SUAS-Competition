import numpy
from math import sqrt

class HoughCircle:
    
    BLOB_RADIUS = 0
    
    def __init__(self, canny_img_in, canny_image_in, radius_bounds_in):
        self.radius_bounds = radius_bounds_in
        self.canny_img = canny_img_in
        self.canny_image = canny_image_in
        self.init_accumulator_matrix()
        self.fill_accumulator_matrix()
    
    def init_accumulator_matrix(self):
        self.accumulator_matrix = numpy.zeros((self.radius_bounds[1] - self.radius_bounds[0], self.canny_img.size[0], self.canny_img.size[1]))
        
            
    def fill_accumulator_matrix(self):
        for radius_add in range(0, self.radius_bounds[1] - self.radius_bounds[0]):
            for x in range(0, self.canny_img.size[0]):
                for y in range(0, self.canny_img.size[1]):
                    if self.canny_image[x,y] != 0:
                        self.vote_pixel_with_radius((x,y), self.radius_bounds[0]+radius_add)
        if HoughCircle.BLOB_RADIUS != 0:
            self.blob_accumulator_matrix()
        
    def blob_accumulator_matrix(self):
        copy_matrix = numpy.zeros(self.accumulator_matrix.shape)
        for radius_index in range(0, self.accumulator_matrix.shape[0]):
            for x in range(HoughCircle.BLOB_RADIUS, self.accumulator_matrix.shape[1] - HoughCircle.BLOB_RADIUS):
                for y in range(HoughCircle.BLOB_RADIUS, self.accumulator_matrix.shape[2] - HoughCircle.BLOB_RADIUS):
                    copy_matrix[radius_index][x][y] = self.get_blob_sum(radius_index, (x,y))
        self.accumulator_matrix = copy_matrix
                    
    def get_blob_sum(self, radius_index, pixel):
        sum = 0
        for x in range(pixel[0]-HoughCircle.BLOB_RADIUS, pixel[0]+HoughCircle.BLOB_RADIUS+1):
            for y in range(pixel[1]-HoughCircle.BLOB_RADIUS, pixel[1]+HoughCircle.BLOB_RADIUS+1):
                if self.pixel_in_bounds((x,y)):
                    sum += self.accumulator_matrix[radius_index][x][y]
        return sum
                    
    def vote_pixel_with_radius(self, pixel, radius):
        radius_index = radius - self.radius_bounds[0]
        for dx in range(-radius, radius):
            dy = int(round( sqrt(radius**2 - dx**2) ))
            point1 = (pixel[0]+dx, pixel[1]+dy)
            point2 = (pixel[0]+dx, pixel[1]-dy)
            if self.pixel_in_bounds(point1):
                self.accumulator_matrix[radius_index][point1[0]][point1[1]] += 1
                #self.fill_blob(radius_index, point1, 1)
            if self.pixel_in_bounds(point2):
                self.accumulator_matrix[radius_index][point2[0]][point2[1]] += 1
                #self.fill_blob(radius_index, point2, 1)
    
    '''def fill_blob(self, radius_index, pixel, increment):
        
        for x in range(pixel[0]-HoughCircle.BLOB_RADIUS, pixel[0]+HoughCircle.BLOB_RADIUS+1):
            for y in range(pixel[1]-HoughCircle.BLOB_RADIUS, pixel[1]+HoughCircle.BLOB_RADIUS+1):
                if self.pixel_in_bounds((x,y)):
                    self.accumulator_matrix[radius_index][x][y] += increment'''
    
    def pixel_in_bounds(self, pixel):
        return pixel[0] > 0 and pixel[0] < self.canny_img.size[0] and pixel[1] > 0 and pixel[1] < self.canny_img.size[1]
        
    def get_highest_vote_num_of_layer(self, radius_index):
        highest_num = 0
        for x in range(0, self.accumulator_matrix.shape[1]):
            for y in range(0, self.accumulator_matrix.shape[2]):
                if self.accumulator_matrix[radius_index][x][y] > highest_num:
                    highest_num = self.accumulator_matrix[radius_index][x][y]
        return highest_num

    def get_highest_vote_and_radius(self):
        highest_vote = 0
        highest_vote_radius_index = 0
        for radius_index in range(0, self.accumulator_matrix.shape[0]):
            highest_vote_in_layer = self.get_highest_vote_num_of_layer(radius_index)
            if highest_vote_in_layer > highest_vote:
                highest_vote = highest_vote_in_layer
                highest_vote_radius_index = radius_index
        return (highest_vote, highest_vote_radius_index + self.radius_bounds[0])
        
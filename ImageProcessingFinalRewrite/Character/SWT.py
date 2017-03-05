import numpy
from math import sin, cos, pi
from PIL import Image
import EdgeProcessing.CannyEdge as CannyEdge

class SWT:
    '''is a constant that is added to the gradient angle for it to 
    raycast into the correct direction to find the next edge'''
    ADD_THETA = pi/4.0
    '''is a minimum stroke value for the vector to be appended to the SWT vectors.
    This will prevent occasions where the raycast will go to an extraneous pixel from canny,
    or hits a very close edge that is not necessary to account for'''
    MINIMUM_STROKE = 3
    
    def __init__(self, sobel_edge_in, canny_img_in, canny_image_in):
        self.sobel_edge = sobel_edge_in
        self.gradient_angles = self.sobel_edge.get_gradient_angles()
        self.canny_img = canny_img_in
        self.canny_image = canny_image_in
        self.init_swt_vectors()
        self.remove_vectors_under_minimum()
        self.init_mean_magnitude()
        self.set_above_mean_to_mean()
        self.swt_vectors = numpy.asarray(self.swt_vectors)
        
    def init_swt_vectors(self):
        self.swt_vectors = []
        
        for x in range(0, self.canny_img.size[0]):
            for y in range(0, self.canny_img.size[1]):
                if self.pixel_is_edge((x,y)):
                    start_pixel = numpy.array([x,y])
                    end_pixel = self.get_end_vector_of_raycast(start_pixel, self.gradient_angles[x][y])
                    if end_pixel != None:
                        append_vector = SWTVector(start_pixel, end_pixel)
                        self.swt_vectors.append(append_vector)
        #self.swt_vectors = numpy.asarray(self.swt_vectors)
                    
                    
    '''given a start point and a gradient angle, will raycast until it sees the next edge or goes out of bounds of
    image. Will return the end point that the raycast lands on if it meets one, and if it doesn't (i.e. goes out of 
    bounds, will return None)'''
    def get_end_vector_of_raycast(self, start_pixel, gradient_angle):
        stroke_width_angle = self.gradient_angles[start_pixel[0]][start_pixel[1]] + SWT.ADD_THETA
        raycast_unit_vector = numpy.array([cos(stroke_width_angle), -sin(stroke_width_angle)])
        '''would be ideal to find a t increment that would traverse all the pixels necessary without counting any 
        of the same ones over again. Try to do this if I have time'''
        curr_pixel = numpy.copy(start_pixel)
        t = 0
        while ((self.pixel_in_bounds(curr_pixel) and not self.pixel_is_edge(curr_pixel)) or numpy.array_equal(curr_pixel, start_pixel)):
            curr_pixel = numpy.floor(numpy.add(start_pixel, raycast_unit_vector * t))
            t += 1
        if self.pixel_is_edge(curr_pixel):
            return curr_pixel
        else:
            return None
    
    def pixel_in_bounds(self, pixel):
        return (pixel[0] >= 0 and pixel[0] < self.canny_img.size[0] and pixel[1] >= 0 and pixel[1] < self.canny_img.size[1])
    
    def pixel_is_edge(self, pixel):
        if self.pixel_in_bounds(pixel):
            return (self.canny_image[pixel[0], pixel[1]] != 0)
        return False
    
    def remove_vectors_under_minimum(self):
        i = 0
        while i < len(self.swt_vectors):
            if self.swt_vectors[i].get_magnitude() < SWT.MINIMUM_STROKE:
                del self.swt_vectors[i]
            else:
                i+=1
                
    def init_mean_magnitude(self):
        sum = 0
        for i in range(0, len(self.swt_vectors)):
            sum += self.swt_vectors[i].get_magnitude()
        self.mean_magnitude = float(sum)/float(len(self.swt_vectors))
    
    def set_above_mean_to_mean(self):
        for i in range(0, len(self.swt_vectors)):
            if self.swt_vectors[i].get_magnitude() > self.mean_magnitude:
                self.swt_vectors[i].set_magnitude(self.mean_magnitude)
    
    def get_pixel_stroke_img(self):
        img = Image.new('L', self.canny_img.size, 0)
        image = img.load()
        for i in range(0, self.swt_vectors.shape[0]):
            self.swt_vectors[i].draw_midpoint_onto_image(image)
        
        '''there are often gaps in between pixels, especially with lower resolution images, in the future, 
        attempt to threshold the image and fill in the gaps somehow. Using canny's thresholding helps, but not much
        as this image has gaps in the vertical and horizontal, whereas my canny's image would have gaps on the diagonals,
        and it is best at filling those'''
        return img
        
    
class SWTVector:
    '''takes two 2d numpy vectors, one for the start position, one for the end position'''
    def __init__(self, start_in, end_in):
        self.start = start_in
        self.end = end_in
        self.travel_vector = numpy.subtract(self.end, self.start)
        self.magnitude = numpy.linalg.norm(self.travel_vector)
        print("swt vector created with magnitude: " + str(self.magnitude))
        self.init_midpoint()
        
    def init_midpoint(self):
        half_travel_vector = numpy.multiply(self.travel_vector, 0.5)
        self.midpoint = numpy.add(self.start, half_travel_vector)
    
    def get_midpoint(self):
        return self.midpoint
    
    def get_magnitude(self):
        return self.magnitude
    
    def set_magnitude(self, magnitude_in):
        unit_vector = numpy.multiply(self.travel_vector, 1.0/self.magnitude)
        self.magnitude = magnitude_in
        self.travel_vector = unit_vector * magnitude_in
        self.end = numpy.add(self.start, numpy.round(unit_vector*magnitude_in))
        self.init_midpoint()
    
    def draw_midpoint_onto_image(self, image):
        midpoint_round = numpy.round(self.midpoint)
        image[midpoint_round[0], midpoint_round[1]] = 255
import numpy
from math import sin, cos, atan2, pi
from Geometry.Rectangle import Rectangle
import ImageOperation.ImageMath as ImageMath
import EdgeProcessing.CannyEdge as CannyEdge



class PolarSideCounter:
    
    THETA_STEP = pi/256.0
    def __init__(self, canny_img_in, canny_image_in):
        self.canny_img = canny_img_in
        self.canny_image = canny_image_in
        self.set_origin()
        self.init_plot()
        self.max_window = 5
        self.append_window_to_plot()
        self.set_mean()
        '''not sure if it is good to set under mean to mean, because there may be a shape that does have
        legitimate maximums that are smaller than the mean'''
        #self.setUnderMeanToMean()
        self.smooth_plot(6, 3)
        
        self.init_maximums()
        self.init_minimums()

    
    def set_origin(self):
        self.origin = ImageMath.get_bw_img_mean_pixel(self.canny_img, self.canny_image)
        self.numpy_origin = numpy.asarray(self.origin)
    
    def init_plot(self):
        self.plot = []
        '''theta = 0
        while theta < 2*pi:
            radius = self.get_radius_of_raycast(theta)
            if radius != None:
                self.plot.append(RadiusAngle(radius, theta))
            theta += PolarSideCounter.THETA_STEP'''
        
        for x in range(0, self.canny_img.size[0]):
            for y in range(0, self.canny_img.size[1]):
                if self.canny_image[x,y] == 255:
                    pix_vector = numpy.array([x,y])
                    vector_from_origin = numpy.subtract(pix_vector, self.numpy_origin)
                    self.plot.append(RadiusAngle(numpy.linalg.norm(vector_from_origin), self.get_raycast_angle(vector_from_origin)))
        self.plot = sorted(self.plot, key = lambda angle: angle.get_angle())
    
    def get_radius_of_raycast(self, theta):
        dxdy = numpy.array([cos(theta), sin(theta)])
        xy = numpy.add(self.numpy_origin, dxdy)
        
        
        while xy[0] > 0 and xy[0] < self.canny_img.size[0] and xy[1] > 0 and xy[1] < self.canny_img.size[1]:
            if self.canny_image[int(xy[0]), int(xy[1])] != 0:
                return numpy.linalg.norm(numpy.subtract(xy, self.numpy_origin))
            xy = numpy.add(xy, dxdy)
        return None
            
    
    def get_raycast_angle(self, vector_from_origin):
        '''y must be negative because of the flipped y axis'''
        angle = atan2(-vector_from_origin[1], vector_from_origin[0])
        if angle < 0:
            angle += 2*pi
        return angle
    
    def get_maximums(self):
        return self.maximums 
    
    def get_minimums(self):
        return self.minimums
    
    def append_window_to_plot(self):
        end_first_slice = self.plot[len(self.plot) - (self.max_window-1)/2 : len(self.plot)]
        begin_last_slice = self.plot[0: (self.max_window-1)/2]
        
        for i in range(0, (self.max_window-1)/2):
            self.plot.insert(i, end_first_slice[i])
        
        for i in range(0, len(begin_last_slice)):
            self.plot.append(begin_last_slice[i])
            
    def set_mean(self):
        self.mean = 0
        for i in range(0, len(self.plot)):
            self.mean += self.plot[i].get_radius()
        self.mean = self.mean/float(len(self.plot))
        
    def setUnderMeanToMean(self):   
        for i in range(0, len(self.plot)):
            if self.plot[i].get_radius() < self.mean:
                self.plot[i].set_radius(self.mean)
    
    def smooth_plot(self, window, numTimes):
        for i in range(0, numTimes):
            for j in range((window-1)/2, len(self.plot) - window/2):
                self.plot[j].set_radius(self.get_mean_in_window(j, window))
                
    def get_mean_in_window(self, index, window):
        sum = 0
        window_count = 0
        while window_count < window:
            sum += self.plot[index - window/2 + window_count].get_radius()
            window_count += 1
            
            #sum += self.plot[i].getRadius()
        return sum/float(window)

    def init_maximums(self):
        self.maximums = []
        for i in range((self.max_window-1)/2, len(self.plot) - (self.max_window-1)/2):
            if self.get_if_is_max_across_num(i, self.max_window):
                self.maximums.append(self.plot[i])
    
    def init_minimums(self):
        self.minimums = []
        for i in range((self.max_window-1)/2, len(self.plot) - (self.max_window-1)/2):
            if self.get_if_is_min_across_num(i, self.max_window):
                self.minimums.append(self.plot[i])
    
    def get_if_is_max_across_num(self, index, num):
        index_count = index - (num-1)/2
        while index_count < index - 1:
            if not(self.plot[index_count].get_radius() < self.plot[index_count + 1].get_radius()):
                return False
            index_count += 1
            if index_count >= len(self.plot):
                index_count -= len(self.plot)
        index_count = index
        
        while index_count < index + (num-1)/2:
            if not(self.plot[index_count].get_radius() > self.plot[index_count + 1].get_radius()):
                return False
            index_count += 1
            if index_count >= len(self.plot):
                index_count -= len(self.plot)
        if not (self.plot[index].get_radius() > self.plot[index-1].get_radius() and self.plot[index].get_radius() > self.plot[index + 1].get_radius()):
            return False
        return True  
    
    def get_if_is_min_across_num(self, index, num):
        index_count = index - (num-1)/2
        while index_count < index - 1:
            if not(self.plot[index_count].get_radius() > self.plot[index_count + 1].get_radius()):
                return False
            index_count += 1
            if index_count >= len(self.plot):
                index_count -= len(self.plot)
        index_count = index
        
        while index_count < index + (num-1)/2:
            if not(self.plot[index_count].get_radius() < self.plot[index_count + 1].get_radius()):
                return False
            index_count += 1
            if index_count >= len(self.plot):
                index_count -= len(self.plot)
        if not (self.plot[index].get_radius() < self.plot[index-1].get_radius() and self.plot[index].get_radius() < self.plot[index + 1].get_radius()):
            return False
        return True    
        
    def get_maximums_drawn_to_img(self):
        img = self.canny_img.copy()
        image = img.load()
        for r_angle in self.maximums:
            r_angle.draw_dot(img, image, self.origin, 255)
        return img
    
    def get_minimums_drawn_to_img(self):
        img = self.canny_img.copy()
        image = img.load()
        for r_angle in self.minimums:
            r_angle.draw_dot(img, image, self.origin, 255)
        return img
    
    def get_origin(self):
        return self.origin
        
class RadiusAngle:
    def __init__(self, radiusIn, angleIn):
        self.radius = radiusIn
        self.angle = angleIn
        
    def get_unit_vector(self):
        return numpy.array([cos(self.angle), sin(self.angle)])
      
    def get_radius(self):
        return self.radius
    
    def set_radius(self, r):
        self.radius = r
    
    def get_angle(self):
        return self.angle    
    
    def sort_key(self):
        return self.angle
    
    def draw_dot(self, img, image, center, color):
        dx = int(self.radius * cos(self.angle))
        dy = int(self.radius * sin(self.angle))
        rect = Rectangle(center[0]+dx - 4, center[1] - dy - 4, 8, 8)
        rect.fill(img, image, color)
        #Drawer.fillRect(img, image, rect, (0,255,0))
        #image[center[0]+dx, center[1]-dy] = (0,255,0)
    
    def get_pixel(self, center):
        dx = int(self.radius * cos(self.angle))
        dy = int(self.radius * sin(self.angle))
        return (center[0] + dx, center[1] - dy)
    
    def __repr__(self):
        return "Angle: " + str(self.angle) + " Radius: " + str(self.radius)
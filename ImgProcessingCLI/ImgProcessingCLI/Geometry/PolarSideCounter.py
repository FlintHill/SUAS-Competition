import numpy
from math import sin, cos, atan2, pi
from ImgProcessingCLI.Geometry import Rectangle
from ImgProcessingCLI.ImageOperation import *
#import matplotlib.pyplot as pyplot

class PolarSideCounter(object):
    THETA_STEP = pi/256.0
    CIRCLE_DERIV_RANGE = (0.96, 1.04)

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

        '''pyplot_r = []
        pyplot_theta = []
        for i in range(2, len(self.plot)-2):
            pyplot_r.append(self.plot[i].get_radius())
            pyplot_theta.append(self.plot[i].get_angle())
        pyplot.plot(pyplot_theta, pyplot_r)
        pyplot.show()'''
        self.smooth_plot(6, 5)

        '''pyplot_r = []
        pyplot_theta = []
        for i in range(2, len(self.plot)-2):
            pyplot_r.append(self.plot[i].get_radius())
            pyplot_theta.append(self.plot[i].get_angle())
        pyplot.plot(pyplot_theta, pyplot_r)
        pyplot.show()'''


        self.set_mean_radius()
        self.set_circle_score()

        self.init_maximums()
        self.init_minimums()

    def set_origin(self):
        self.origin = get_bw_img_mean_pixel(self.canny_img, self.canny_image)
        self.numpy_origin = numpy.asarray(self.origin)

    def init_plot(self):
        self.plot = []

        for x in range(0, self.canny_img.size[0]):
            for y in range(0, self.canny_img.size[1]):
                if self.canny_image[x,y] == 255:
                    pix_vector = numpy.array([x,y])
                    vector_from_origin = numpy.subtract(pix_vector, self.numpy_origin)
                    self.plot.append(RadiusAngle(numpy.linalg.norm(vector_from_origin), self.get_raycast_angle(vector_from_origin), vector_from_origin))
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
        end_first_slice = self.plot[len(self.plot) - int((self.max_window-1)/2) : len(self.plot)]
        begin_last_slice = self.plot[0: int((self.max_window-1)/2)]

        for i in range(0, int((self.max_window-1)/2)):
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
            for j in range(int((window-1)/2), len(self.plot) - int(window/2)):
                self.plot[j].set_radius(self.get_mean_in_window(j, window))

    def get_mean_in_window(self, index, window):
        sum = 0
        window_count = 0
        while window_count < window:
            sum += self.plot[index - int(window/2) + window_count].get_radius()
            window_count += 1

            #sum += self.plot[i].getRadius()
        return sum/float(window)

    def init_maximums(self):
        self.maximums = []
        for i in range(int((self.max_window-1)/2), len(self.plot) - int((self.max_window-1)/2)):
            if self.get_if_is_max_across_num(i, self.max_window):
                self.maximums.append(self.plot[i])

    def init_minimums(self):
        self.minimums = []
        for i in range(int((self.max_window-1)/2), len(self.plot) - int((self.max_window-1)/2)):
            if self.get_if_is_min_across_num(i, self.max_window):
                self.minimums.append(self.plot[i])

    def get_if_is_max_across_num(self, index, num):
        index_count = index - int((num-1)/2)
        while index_count < index - 1:
            if not(self.plot[index_count].get_radius() < self.plot[index_count + 1].get_radius()):
                return False
            index_count += 1
            if index_count >= len(self.plot):
                index_count -= len(self.plot)
        index_count = index

        while index_count < index + int((num-1)/2):
            if not(self.plot[index_count].get_radius() > self.plot[index_count + 1].get_radius()):
                return False
            index_count += 1
            if index_count >= len(self.plot):
                index_count -= len(self.plot)
        if not (self.plot[index].get_radius() > self.plot[index-1].get_radius() and self.plot[index].get_radius() > self.plot[index + 1].get_radius()):
            return False
        return True

    def get_if_is_min_across_num(self, index, num):
        index_count = index - int((num-1)/2)
        while index_count < index - 1:
            if not(self.plot[index_count].get_radius() > self.plot[index_count + 1].get_radius()):
                return False
            index_count += 1
            if index_count >= len(self.plot):
                index_count -= len(self.plot)
        index_count = index

        while index_count < index + int((num-1)/2):
            if not(self.plot[index_count].get_radius() < self.plot[index_count + 1].get_radius()):
                return False
            index_count += 1
            if index_count >= len(self.plot):
                index_count -= len(self.plot)
        if not (self.plot[index].get_radius() < self.plot[index-1].get_radius() and self.plot[index].get_radius() < self.plot[index + 1].get_radius()):
            return False
        return True

    def set_mean_radius(self):
        self.mean_radius = 0
        for i in range(int((self.max_window-1)/2), len(self.plot) - int((self.max_window-1)/2)):
            self.mean_radius += self.plot[i].get_radius()
        self.mean_radius = self.mean_radius / float(len(self.plot))

    def set_circle_score(self):
        '''this needs to be optimized because pulling the vector is something that could be set
        in initializing the plot rather than having to recalculate'''
        x_deriv = numpy.zeros((len(self.plot)))
        y_deriv = numpy.zeros((len(self.plot)))
        for i in range(1, x_deriv.shape[0]):
            prev_vector = self.plot[i-1].get_vector()
            vector = self.plot[i].get_vector()
            d_theta = self.plot[i].get_angle() - self.plot[i-1].get_angle()
            if d_theta != 0:
                x_deriv[i] = (vector[0] - prev_vector[0])/d_theta
                y_deriv[i] = (vector[1] - prev_vector[1])/d_theta
            elif i != 0:
                x_deriv[i] = x_deriv[i-1]
                y_deriv[i] = y_deriv[i-1]

        #x_deriv = numpy.gradient(x_deriv)/self.mean_radius
        #y_deriv = numpy.gradient(y_deriv)/self.mean_radius
        x_deriv = x_deriv/self.mean_radius
        y_deriv = y_deriv/self.mean_radius

        mag_derivs = numpy.sqrt(numpy.add(numpy.square(x_deriv), numpy.square(y_deriv)))

        num_matches = 0
        for i in range(0, mag_derivs.shape[0]):
            if mag_derivs[i] >= PolarSideCounter.CIRCLE_DERIV_RANGE[0] and mag_derivs[i] <= PolarSideCounter.CIRCLE_DERIV_RANGE[1]:
                num_matches += 1
        self.circle_score = float(num_matches)/float(mag_derivs.shape[0])
        #self.circle_score = .5

    def get_circle_score(self):
        return self.circle_score

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

class RadiusAngle(object):

    def __init__(self, radiusIn, angleIn, vector):
        self.radius = radiusIn
        self.angle = angleIn
        self.vector = vector

    def get_unit_vector(self):
        return numpy.array([cos(self.angle), sin(self.angle)])

    def get_vector(self):
        return self.vector

    def get_radius(self):
        return self.radius

    def set_radius(self, r):
        radius_ratio = r/self.radius
        self.vector = self.vector * radius_ratio
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

    def __getitem__(self, index):
        if index == 0:
            return self.radius
        return self.angle

    def __repr__(self):
        return "Angle: " + str(self.angle) + " Radius: " + str(self.radius)

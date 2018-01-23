import matplotlib.pyplot
from get_origin import get_origin
from PIL import Image, ImageOps
import numpy
import math

import plotly.plotly as py
import plotly.graph_objs as go
import peakutils

class PolarSideCounter(object):

    def __init__(self, canny_img, show_plot=False):
        self.canny_img = canny_img
        self.loaded_img = self.canny_img.load()

        self.show_plot=show_plot

        self.origin = get_origin(self.canny_img)
        self.numpy_origin = numpy.asarray(self.origin)

        self.raycast_plot()
        self.smooth_plot(6, 5) #NEEDS TO BE OPTOMIZED
        self.set_maximums() #NEEDS TO BE OPTOMIZED
        self.set_circle_score()

    def raycast_plot(self):
        self.plot = []
        for x in range(0, self.canny_img.size[0]):
            for y in range(0, self.canny_img.size[1]):
                if self.loaded_img[x,y] == 255:
                    distance_vector = numpy.subtract(numpy.array([x,y]), self.numpy_origin)
                    distance_from_origin = math.hypot(distance_vector[0], distance_vector[1])

                    angle = math.atan2(-distance_vector[1], distance_vector[0])
                    if angle < 0:
                        angle += 2*math.pi

                    self.plot.append((angle, distance_from_origin, distance_vector))
                    self.plot = sorted(self.plot, key=lambda a:a[0])

    def smooth_plot(self, window, iterations):
        for i in range(0, iterations):
            for j in range(int((window-1)/2), len(self.plot) - int(window/2)):
                self.plot[j] = (self.plot[j][0], self.get_mean_in_window(j, window), self.plot[j][2])

    def get_mean_in_window(self, index, window):
        total = 0
        window_count = 0
        while window_count < window:
            total += self.plot[index - int(window/2) + window_count][1]
            window_count += 1

        return total/float(window)

    def set_maximums(self):
        x, y, z = zip(*self.plot)
        x=numpy.array(x)
        y=numpy.array(y)

        base = peakutils.baseline(y, 2)

        indices = peakutils.indexes(numpy.subtract(y,base), thres=0.5, min_dist=10)
        self.polar_side_maximums = len(indices)

        if self.show_plot:
            plot_trace = go.Scatter(
                x=x,
                y=numpy.subtract(y,base),
                mode='lines',
                name='Original Plot',
            )
            maximums_trace = go.Scatter(
                x=[x[i] for i in indices],
                y=[y[j]-base[j] for j in indices],
                mode='markers',
                marker=dict(
                    size=8,
                    color='rgb(255,0,0)',
                    symbol='cross'
                ),
                name='Detected Maximums'
            )
            data = [plot_trace, maximums_trace]
            py.plot(data, filename='psc')

    def set_circle_score(self):
        """
        Adapted from ImgProcessingCLI's PolarSideCounter by Peter Husisian
        """
        CIRCLE_DERIV_RANGE = (0.96, 1.04)
        self.mean_radius = 0
        for i in range(len(self.plot)):
            self.mean_radius += self.plot[i][1]
        self.mean_radius = self.mean_radius / float(len(self.plot))
        x_deriv = numpy.zeros((len(self.plot)))
        y_deriv = numpy.zeros((len(self.plot)))
        for i in range(1, x_deriv.shape[0]):
            prev_vector = self.plot[i-1][2]
            vector = self.plot[i][2]
            d_theta = self.plot[i][0] - self.plot[i-1][0]
            if d_theta != 0:
                x_deriv[i] = (vector[0] - prev_vector[0])/d_theta
                y_deriv[i] = (vector[1] - prev_vector[1])/d_theta
            elif i != 0:
                x_deriv[i] = x_deriv[i-1]
                y_deriv[i] = y_deriv[i-1]

        x_deriv = x_deriv/self.mean_radius
        y_deriv = y_deriv/self.mean_radius

        mag_derivs = numpy.sqrt(numpy.add(numpy.square(x_deriv), numpy.square(y_deriv)))

        num_matches = 0
        for i in range(0, mag_derivs.shape[0]):
            if mag_derivs[i] >= CIRCLE_DERIV_RANGE[0] and mag_derivs[i] <= CIRCLE_DERIV_RANGE[1]:
                num_matches += 1
        self.circle_score = float(num_matches)/float(mag_derivs.shape[0])

    def get_polar_side_maximums(self):
        return self.polar_side_maximums

    def get_origin(self):
        return self.origin

    def get_circle_score(self):
        return self.circle_score

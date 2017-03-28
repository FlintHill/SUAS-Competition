from PIL import Image
from math import atan2
from ImgProcessingCLI.KernelOperations import *
import numpy

class SobelEdge(object):

    '''these are the 3x3 sobel kernels for x and y'''
    SOBEL_KERNEL_X = [[-1,0,1],[-2,0,2],[-1,0,1]]
    SOBEL_KERNEL_Y = [[-1,-2,-1],[0,0,0],[1,2,1]]

    '''assumes the img is already converted to grayscale'''
    def __init__(self, img_in):
        self.img = img_in
        self.image = self.img.load()
        self.init_gradients()
        self.init_gradient_mags()
        self.init_gradient_mag_img()
        self.init_gradient_angles()

    def init_gradients(self):
        self.gradient_x = convolute_array(self.img, SobelEdge.SOBEL_KERNEL_X)
        self.gradient_y = convolute_array(self.img, SobelEdge.SOBEL_KERNEL_Y)

    def init_gradient_mags(self):
        self.gradient_mags = numpy.zeros((len(self.gradient_x), len(self.gradient_x[0])))
        for i in range(0, self.gradient_mags.shape[0]):
            for j in range(0, self.gradient_mags.shape[1]):
                mag_vector = numpy.array([self.gradient_x[i][j], self.gradient_y[i][j]])
                self.gradient_mags[i][j] = numpy.linalg.norm(mag_vector)

    def init_gradient_mag_img(self):
        '''array is transposed in fromarray because the output image would be mirrored across y/x'''
        self.gradient_mag_img = Image.fromarray(numpy.transpose(self.gradient_mags))

    def init_gradient_angles(self):
        self.gradient_angles = numpy.zeros((len(self.gradient_x), len(self.gradient_x[0])))
        for x in range(0, len(self.gradient_x)):
            for y in range(0, len(self.gradient_x[0])):
                self.gradient_angles[x][y] = atan2(self.gradient_y[x][y], self.gradient_x[x][y])

    def get_img_gradient_under_threshold(self, threshold):
        out_img = Image.new("L", self.gradient_mag_img.size, 0)
        out_image = out_img.load()
        for x in range(0, self.gradient_mags.shape[0]):
            for y in range(0, self.gradient_mags.shape[1]):
                if self.gradient_mags[x][y] <= threshold:
                    out_image[x,y] = 255
        return out_img

    def get_gradient_mags(self):
        return self.gradient_mags

    def get_gradient_angles(self):
        return self.gradient_angles

    def get_gradient_mag_img(self):
        return self.gradient_mag_img

    def get_x_gradient(self):
        return self.gradient_x

    def get_y_gradient(self):
        return self.gradient_y

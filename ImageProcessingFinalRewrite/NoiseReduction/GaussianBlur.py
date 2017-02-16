from PIL import Image
import numpy
from math import pi, exp
import KernelOperations.KernelMath as KernelMath

def get_gaussian_filtered_bw_img(img, image, kernel_size, std_dev):
    gauss_kernel = get_gaussian_kernel(kernel_size, std_dev)
    return KernelMath.convolute(img, gauss_kernel)

def get_gaussian_kernel(kernel_size, std_dev):
    kernel = [[float(1.0/(2.0 * pi * std_dev**2)) for j in range(0, kernel_size)] for i in range(0, kernel_size)]
    kernel_x = 0
    kernel_y = 0
    kernel_margin = (kernel_size - 1)/2
    for x in range(-kernel_margin, kernel_margin + 1):
        for y in range(-kernel_margin, kernel_margin + 1):
            numerator = float(x**2 + y**2)
            denominator = 2.0 * std_dev**2
            kernel[kernel_x][kernel_y] *= exp(numerator/denominator)
            kernel_y += 1
        kernel_y = 0
        kernel_x += 1
    
    sum = numpy.sum(numpy.array(kernel))
    print(sum)
    for x in range(0, len(kernel)):
        for y in range(0, len(kernel[0])):
            kernel[x][y] /= sum
    
    return kernel
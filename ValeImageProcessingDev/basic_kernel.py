from PIL import Image
import itertools
from math import pi, exp
import numpy as np

def get_gaussian_kernel(kernel_size, sd):
    """
    Create a gaussian kernel with the given size and standard deviation
    """
    kernel = [[float(1.0/2 * sd**2 * pi) for j in range(kernel_size)] for i in range(kernel_size)]

    kernel_x = 0
    kernel_y = 0
    kernel_midpoint = int((kernel_size - 1) / 2)
    for x in range(-kernel_midpoint, kernel_midpoint + 1):
        for y in range(-kernel_midpoint, kernel_midpoint + 1):
            numerator = float(x**2 + y**2)
            denominator = 2.0 * sd
            kernel[kernel_x][kernel_y] = exp(numerator/denominator)
            kernel_y += 1
        kernel_y = 0
        kernel_x += 1

    return kernel

def get_mean_blur_kernel(kernel_size):
    """
    Create a mean blur kernel given a size
    """
    kernel = [[1 for j in range(kernel_size)] for i in range(kernel_size)]

    return kernel

def convolute(img, kernel):
    """
    Apply a blur to an image
    """
    kernel_sum = sum(itertools.chain.from_iterable(kernel))
    kernel_size = len(kernel) // 2

    img_map = img.load()
    blurred_img = img.copy()

    calc_index = 0
    total_calcs = (img.size[0] - (2 * kernel_size)) * (img.size[1] - (2 * kernel_size))
    for y_index in range(kernel_size, img.size[0] - kernel_size):
        for x_index in range(kernel_size, img.size[1] - kernel_size):
            calc_index += 1
            print("Percent Complete: " + str(100 * float(calc_index) / float(total_calcs)))

            component_sum = np.zeros(3)
            for outer_index in range(len(kernel)):
                for inner_index in range(len(kernel)):
                    component_sum += np.array(img_map[y_index + inner_index - kernel_size, x_index + outer_index - kernel_size][:3])

            component_sum = component_sum // kernel_sum
            component_sum_list = component_sum.tolist()
            for index in range(len(component_sum_list)):
                component_sum_list[index] = int(component_sum_list[index])

            blurred_img.putpixel([y_index, x_index], tuple(component_sum_list))

    return blurred_img

im = Image.open("data/test.png")
#im.show()
#apply_blur(im, get_gaussian_kernel(3,3)).show()
convolute(im, get_mean_blur_kernel(2)).show()
#gaussian_blur(im, get_gaussian_kernel(5, 6)).show()
#mean_blur(im).show()

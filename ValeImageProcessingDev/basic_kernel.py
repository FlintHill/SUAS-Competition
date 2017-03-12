from PIL import Image
import itertools
from math import pi, exp

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

def gaussian_blur(img, kernel):
    """
    Gaussian Blur an image
    """
    kernel_sum = sum(itertools.chain.from_iterable(kernel))

    img_map = img.load()
    blurred_img = img.copy()

    calc_index = 0
    total_calcs = (img.size[0] - 2) * (img.size[1] - 2)
    for y_index in range(2, img.size[0] - 2):
        for x_index in range(2, img.size[1] - 2):
            calc_index += 1
            print("Percent Complete: " + str(100 * float(calc_index) / float(total_calcs)))

            component_sum = [0,0,0]
            for outer_index in range(len(kernel)):
                for inner_index in range(len(kernel[0])):
                    component_sum[0] += img_map[y_index - 2 + inner_index, x_index - 2 + outer_index][0]
                    component_sum[1] += img_map[y_index - 2 + inner_index, x_index - 2 + outer_index][1]
                    component_sum[2] += img_map[y_index - 2 + inner_index, x_index - 2 + outer_index][2]
            component_sum[0] = int(component_sum[0] / kernel_sum)
            component_sum[1] = int(component_sum[1] / kernel_sum)
            component_sum[2] = int(component_sum[2] / kernel_sum)

            blurred_img.putpixel([y_index, x_index], tuple(component_sum))

    return blurred_img

def mean_blur(img):
    """
    Mean blur an image
    """
    kernel = [[1,1,1],[1,1,1],[1,1,1]]
    kernel_sum = sum(itertools.chain.from_iterable(kernel))

    img_map = img.load()
    blurred_img = img.copy()

    calc_index = 0
    total_calcs = (img.size[0] - 2) * (img.size[1] - 2)
    for y_index in range(1, img.size[0] - 1):
        for x_index in range(1, img.size[1] - 1):
            calc_index += 1
            print("Percent Complete: " + str(100 * float(calc_index) / float(total_calcs)))

            component_sum = [0,0,0]
            for outer_index in range(len(kernel)):
                for inner_index in range(len(kernel[0])):
                    component_sum[0] += img_map[y_index - 1 + inner_index, x_index - 1 + outer_index][0]
                    component_sum[1] += img_map[y_index - 1 + inner_index, x_index - 1 + outer_index][1]
                    component_sum[2] += img_map[y_index - 1 + inner_index, x_index - 1 + outer_index][2]
            component_sum[0] = int(component_sum[0] / kernel_sum)
            component_sum[1] = int(component_sum[1] / kernel_sum)
            component_sum[2] = int(component_sum[2] / kernel_sum)

            blurred_img.putpixel([y_index, x_index], tuple(component_sum))

    return blurred_img

im = Image.open("data/test.png")
#im.show()
gaussian_blur(im, get_gaussian_kernel(5, 6)).show()
#mean_blur(im).show()

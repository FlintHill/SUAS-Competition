from ImgProcessingCLI.NoiseReduction import *
import numpy
from math import pi, cos, sin, atan2
from ImgProcessingCLI.EdgeProcessing import *

A_CONSTANT = 0.04 #is a constant that is necessary for harris corner. Can be a value from 0.04 to 0.1. See the harris operator formula for example of A

def get_corners_over_threshold(sobel_edge, kernel_size, std_dev, thresh):
    sobel_img = sobel_edge.get_gradient_mag_img()
    gaussian_kernel = get_gaussian_kernel(kernel_size, std_dev)
    corner_scores = get_corner_scores(sobel_edge, gaussian_kernel)
    corner_maximums = get_corner_score_maximums(sobel_edge, corner_scores)
    i = 0
    while i < len(corner_maximums):
        if not corner_scores[corner_maximums[i][0]][corner_maximums[i][1]] > thresh:
            del corner_maximums[i]
        else:
            i+=1
    return corner_maximums

def draw_corners(corners, image, color):
    for i in range(0, len(corners)):
        image[corners[i][0], corners[i][1]] = color

def get_corner_scores(sobel_edge, kernel):
    sobel_img = sobel_edge.get_gradient_mag_img()
    corner_scores = numpy.empty((sobel_img.size[0], sobel_img.size[1]))
    init_offset = int((len(kernel)-1)/2)
    for x in range(init_offset, sobel_img.size[0] - init_offset):
        for y in range(init_offset, sobel_img.size[1] - init_offset):
            second_moment_matrix = get_second_moment_matrix(sobel_edge, (x,y), kernel)
            corner_scores[x][y] = numpy.linalg.det(second_moment_matrix) - (numpy.trace(second_moment_matrix)**2)*A_CONSTANT
    return corner_scores

def get_second_moment_matrix(sobel_edge, pixel, kernel):
    sum = numpy.array([0,0])
    kernel_size = len(kernel)
    init_offset = int((kernel_size-1)/2)
    kernel_x = 0
    kernel_y = 0
    for x in range(pixel[0]-init_offset, pixel[0]+init_offset + 1):
        for y in range(pixel[1]-init_offset, pixel[1]+init_offset+1):
            moment_matrix_at_point = get_second_moment_matrix_at_point(sobel_edge, (x, y))
            sum = numpy.add(sum, numpy.multiply(moment_matrix_at_point, kernel[kernel_x][kernel_y]))
            kernel_y += 1
        kernel_y = 0
        kernel_x += 1
    return sum

def get_second_moment_matrix_at_point(sobel_edge, pixel):
    gradient = numpy.array([sobel_edge.get_x_gradient()[pixel[0]][pixel[1]], sobel_edge.get_y_gradient()[pixel[0]][pixel[1]]])
    matrix_at_point = numpy.array([[gradient[0]**2, gradient[0]*gradient[1]],
                                   [gradient[0]*gradient[1], gradient[1]**2]])
    return matrix_at_point

'''may need to work on making this a bit better -- unfortunately have to copy paste some code from canny's
non-maximum supression'''
def get_corner_score_maximums(sobel_edge, corner_scores):
    corners = []
    gradient_angles = sobel_edge.get_gradient_angles()

    for x in range(int(CANNY_RADIUS), corner_scores.shape[0] - int(CANNY_RADIUS)):
        for y in range(int(CANNY_RADIUS), corner_scores.shape[1] - int(CANNY_RADIUS)):
            if pixel_is_max_across_edge(corner_scores, (x,y), gradient_angles[x][y]):
                corners.append((x,y))
    return corners

def pixel_is_max_across_edge(corner_scores, pixel, angle):
    perp_angle = angle + (pi/4.0)
    neighbor_pixels = get_neighboring_edge_pixel_mags(corner_scores, pixel, perp_angle)
    return (corner_scores[pixel[0]][pixel[1]] > neighbor_pixels[0] and corner_scores[pixel[0]][pixel[1]] > neighbor_pixels[1])

def get_neighboring_edge_pixel_mags(corner_scores, pixel, perp_angle):
    xComp = CANNY_RADIUS * cos(perp_angle)
    yComp = CANNY_RADIUS * sin(perp_angle)
    dx = 0
    dy = 0
    if yComp > -CANNY_VAL_45_DEG and yComp < CANNY_VAL_45_DEG:
        dy = 0
    elif yComp >= CANNY_VAL_45_DEG:
        dy = 1
    elif yComp <= -CANNY_VAL_45_DEG:
        dy = -1

    if xComp > -CANNY_VAL_45_DEG and xComp < CANNY_VAL_45_DEG:
        dx = 0
    elif xComp >= CANNY_VAL_45_DEG:
        dx = 1
    elif xComp <= -CANNY_VAL_45_DEG:
        dx = -1
    firstPixel = (pixel[0] + dx, pixel[1] - dy)
    secondPixel = (pixel[0] - dx, pixel[1] + dy)
    return (corner_scores[firstPixel[0]][firstPixel[1]], corner_scores[secondPixel[0]][secondPixel[1]])

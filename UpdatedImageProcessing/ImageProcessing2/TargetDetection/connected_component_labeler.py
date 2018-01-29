"""
Target Detection currently does not need this method.
"""
import sys
import cv2
import copy
import numpy
from PIL import Image
from collections import Counter
from .list_operations import ListOperations
from .color_operations import ColorOperations

class ConnectedComponentLabeler(object):

    @staticmethod
    def label_connected_components(single_target_crop):
        """
        Return the boundary of the target in the given crop.

        :param single_target_crop: a captured image of a potential target.

        :type single_target_crop: an image file such as JPG and PNG.
        """
        index_matrix = []
        pixel_access_single_target_crop = single_target_crop.load()

        for y in range(single_target_crop.height):
            index_matrix.append([])

            for x in range(single_target_crop.width):
                index_matrix[y].append(0)

                if (y == 0):
                    if (x == 0):
                        index_matrix[y][x] = 0

                if (y != 0):
                    current_pixel_color = pixel_access_single_target_crop[x, y]
                    above_pixel_color = pixel_access_single_target_crop[x, y - 1]
                    vertical_color_difference = ColorOperations.find_percentage_difference(current_pixel_color, above_pixel_color)

                    if (vertical_color_difference <= 15):
                        index_matrix[y][x] = index_matrix[y - 1][x]

                if (x != 0):
                    current_pixel_color = pixel_access_single_target_crop[x, y]
                    left_pixel_color = pixel_access_single_target_crop[x - 1, y]
                    horizontal_color_difference = ColorOperations.find_percentage_difference(current_pixel_color, left_pixel_color)

                    if (horizontal_color_difference > 15):
                        index_matrix[y][x] = index_matrix[y][x - 1] + 1

        second_most_common_element = ListOperations.find_2nd_most_common_element_from_2d_list(index_matrix)

        x_min = sys.maxint
        y_min = sys.maxint
        x_max = -1
        y_max = -1

        for y in range(len(index_matrix)):
            for x in range(len(index_matrix[y])):
                if (index_matrix[y][x] == second_most_common_element):
                    if (x < x_min):
                        x_min = x
                    if (x > x_max):
                        x_max = x
                    if (y < y_min):
                        y_min = y
                    if (y > y_max):
                        y_max = y

        return (x_min - 15, y_min - 15, x_max + 15, y_max - 15)

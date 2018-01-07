from PIL import Image

class TargetAnalyzer(object):

    @staticmethod
    def find_target_average_color(target_map_image, target_location):
        """
        Find the average color of a target by taking the average RGB value of
        nine uniformly separated pixels within this target and return this average
        RGB value as a color of 3-tuple.

        :param target_map_image: the image of the background
        :param target_location: the information of a single target

        :type target_map_image: PIL image
        :type target_location: a list containing four elements for each
                               target: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        pixel_access_target_map_image = target_map_image.load()

        center_color = pixel_access_target_map_image[target_location[0] + (target_location[2] / 2), target_location[1] + (target_location[3] / 2)]

        upper_color_1 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 2), target_location[1] + (target_location[3] / 6)]
        upper_color_2 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 2), target_location[1] + (target_location[3] / 3)]

        lower_color_1 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 2), target_location[1] + (target_location[3] / 6 * 5)]
        lower_color_2 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 2), target_location[1] + (target_location[3] / 3 * 2)]

        left_color_1 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6), target_location[1] + (target_location[3] / 2)]
        left_color_2 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3), target_location[1] + (target_location[3] / 2)]

        right_color_1 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6 * 5), target_location[1] + (target_location[3] / 2)]
        right_color_2 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3 * 2), target_location[1] + (target_location[3] / 2)]

        left_upper_color_1 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6), target_location[1] + (target_location[3] / 6)]
        left_upper_color_2 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3), target_location[1] + (target_location[3] / 6)]
        left_upper_color_3 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6), target_location[1] + (target_location[3] / 3)]
        left_upper_color_4 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3), target_location[1] + (target_location[3] / 3)]

        right_upper_color_1 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3 * 2), target_location[1] + (target_location[3] / 6)]
        right_upper_color_2 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6 * 5), target_location[1] + (target_location[3] / 6)]
        right_upper_color_3 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3 * 2), target_location[1] + (target_location[3] / 3)]
        right_upper_color_4 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6 * 5), target_location[1] + (target_location[3] / 3)]

        left_lower_color_1 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6), target_location[1] + (target_location[3] / 3 * 2)]
        left_lower_color_2 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3), target_location[1] + (target_location[3] / 3 * 2)]
        left_lower_color_3 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6), target_location[1] + (target_location[3] / 6 * 5)]
        left_lower_color_4 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3), target_location[1] + (target_location[3] / 6 * 5)]

        right_lower_color_1 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3 * 2), target_location[1] + (target_location[3] / 3 * 2)]
        right_lower_color_2 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6 * 5), target_location[1] + (target_location[3] / 3 * 2)]
        right_lower_color_3 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 3 * 2), target_location[1] + (target_location[3] / 6 * 5)]
        right_lower_color_4 = pixel_access_target_map_image[target_location[0] + (target_location[2] / 6 * 5), target_location[1] + (target_location[3] / 6 * 5)]

        average_target_color_x = (center_color[0] + upper_color_1[0] + upper_color_2[0] + lower_color_1[0] + lower_color_2[0] + left_color_1[0] + left_color_2[0] + right_color_1[0] + right_color_2[0]\
                                + left_upper_color_1[0] + left_upper_color_2[0] + left_upper_color_3[0] + left_upper_color_4[0] + right_upper_color_1[0] + right_upper_color_2[0] + right_upper_color_3[0] + right_upper_color_4[0]\
                                + left_lower_color_1[0] + left_lower_color_2[0] + left_lower_color_3[0] + left_lower_color_4[0] + right_lower_color_1[0] + right_lower_color_2[0] + right_lower_color_3[0] + right_lower_color_4[0]) / 25

        average_target_color_y = (center_color[1] + upper_color_1[1] + upper_color_2[1] + lower_color_1[1] + lower_color_2[1] + left_color_1[1] + left_color_2[1] + right_color_1[1] + right_color_2[1]\
                                + left_upper_color_1[1] + left_upper_color_2[1] + left_upper_color_3[1] + left_upper_color_4[1] + right_upper_color_1[1] + right_upper_color_2[1] + right_upper_color_3[1] + right_upper_color_4[1]\
                                + left_lower_color_1[1] + left_lower_color_2[1] + left_lower_color_3[1] + left_lower_color_4[1] + right_lower_color_1[1] + right_lower_color_2[1] + right_lower_color_3[1] + right_lower_color_4[1]) / 25

        average_target_color_z = (center_color[2] + upper_color_1[2] + upper_color_2[2] + lower_color_1[2] + lower_color_2[2] + left_color_1[2] + left_color_2[2] + right_color_1[2] + right_color_2[2]\
                                + left_upper_color_1[2] + left_upper_color_2[2] + left_upper_color_3[2] + left_upper_color_4[2] + right_upper_color_1[2] + right_upper_color_2[2] + right_upper_color_3[2] + right_upper_color_4[2]\
                                + left_lower_color_1[2] + left_lower_color_2[2] + left_lower_color_3[2] + left_lower_color_4[2] + right_lower_color_1[2] + right_lower_color_2[2] + right_lower_color_3[2] + right_lower_color_4[2]) / 25

        average_target_color = (average_target_color_x, average_target_color_y, average_target_color_z)

        return average_target_color

    @staticmethod
    def find_surrounding_average_color(target_map_image, target_location):
        """
        Find the average color of the surrounding color of a target by taking the
        average RGB value of eight uniformly separated pixels around this target
        and return this average RGB value as a color of 3-tuple.

        :param target_map_image: the image of the background
        :param target_location: the information of a single target

        :type target_map_image: PIL image
        :type target_location: a list containing four elements for each
                               target: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        left_x = target_location[0] - (target_location[2] / 4)
        right_x = target_location[0] + target_location[2] + (target_location[2] / 4)
        upper_y = target_location[1] - (target_location[3] / 4)
        lower_y = target_location[1] + target_location[3] + (target_location[3] / 4)

        if (left_x < 0):
            left_x = 0

        if (right_x >= target_map_image.width):
            right_x = target_map_image.width - 1

        if (upper_y < 0):
            upper_y = 0

        if (lower_y >= target_map_image.height):
            lower_y = target_map_image.height - 1

        pixel_access_target_map_image = target_map_image.load()

        upper_color = pixel_access_target_map_image[target_location[0] + (target_location[2] / 2), upper_y]
        lower_color = pixel_access_target_map_image[target_location[0] + (target_location[2] / 2), lower_y]
        left_color = pixel_access_target_map_image[left_x, target_location[1] + (target_location[3] / 2)]
        right_color = pixel_access_target_map_image[right_x, target_location[1] + (target_location[3] / 2)]

        left_upper_color = pixel_access_target_map_image[left_x, upper_y]
        right_upper_color = pixel_access_target_map_image[right_x, upper_y]
        left_lower_color = pixel_access_target_map_image[left_x, lower_y]
        right_lower_color = pixel_access_target_map_image[right_x, lower_y]

        average_surrounding_color_x = (upper_color[0] + lower_color[0] + left_color[0] + right_color[0] + left_upper_color[0] + right_upper_color[0] + left_lower_color[0] + right_lower_color[0]) / 8
        average_surrounding_color_y = (upper_color[1] + lower_color[1] + left_color[1] + right_color[1] + left_upper_color[1] + right_upper_color[1] + left_lower_color[1] + right_lower_color[1]) / 8
        average_surrounding_color_z = (upper_color[2] + lower_color[2] + left_color[2] + right_color[2] + left_upper_color[2] + right_upper_color[2] + left_lower_color[2] + right_lower_color[2]) / 8
        average_surrounding_color = (average_surrounding_color_x, average_surrounding_color_y, average_surrounding_color_z)

        return average_surrounding_color

    @staticmethod
    def find_rim_average_color(cropped_target_image):
        pixel_access_cropped_target_image = cropped_target_image.load()
        first_two_line_colors = []
        last_two_line_colors = []
        first_two_column_colors = []
        last_two_column_colors = []

        for x in range(cropped_target_image.width):
            first_two_line_colors.append(pixel_access_cropped_target_image[x, 0])
            first_two_line_colors.append(pixel_access_cropped_target_image[x, 1])
            last_two_line_colors.append(pixel_access_cropped_target_image[x, cropped_target_image.height - 1])
            last_two_line_colors.append(pixel_access_cropped_target_image[x, cropped_target_image.height - 2])

        for y in range(1, cropped_target_image.height - 1):
            first_two_column_colors.append(pixel_access_cropped_target_image[0, y])
            first_two_column_colors.append(pixel_access_cropped_target_image[1, y])
            last_two_column_colors.append(pixel_access_cropped_target_image[cropped_target_image.width - 1, y])
            last_two_column_colors.append(pixel_access_cropped_target_image[cropped_target_image.width - 2, y])

        rim_colors = first_two_line_colors + last_two_line_colors + first_two_column_colors + last_two_column_colors
        number_of_colors = len(rim_colors)

        r_sum = 0
        g_sum = 0
        b_sum = 0

        for index in range(len(rim_colors)):
            r_sum += rim_colors[index][0]
            g_sum += rim_colors[index][1]
            b_sum += rim_colors[index][2]

        r_average = float(r_sum) / number_of_colors
        g_average = float(g_sum) / number_of_colors
        b_average = float(b_sum) / number_of_colors

        return (r_average, g_average, b_average)

    @staticmethod
    def find_average_corner_color(cropped_target_image):
        pixel_access_cropped_target_image = cropped_target_image.load()

        upper_left_corner_color = pixel_access_cropped_target_image[1, 1]
        upper_right_corner_color = pixel_access_cropped_target_image[cropped_target_image.width - 2, 1]
        lower_left_corner_color = pixel_access_cropped_target_image[1, cropped_target_image.height - 2]
        lower_right_corner_color = pixel_access_cropped_target_image[cropped_target_image.width - 2, cropped_target_image.height - 2]

        cropped_target_image_average_corner_color_x = (upper_left_corner_color[0] + upper_right_corner_color[0]\
                                                        + lower_left_corner_color[0] + lower_right_corner_color[0]) / 4

        cropped_target_image_average_corner_color_y = (upper_left_corner_color[1] + upper_right_corner_color[1]\
                                                        + lower_left_corner_color[1] + lower_right_corner_color[1]) / 4

        cropped_target_image_average_corner_color_z = (upper_left_corner_color[2] + upper_right_corner_color[2]\
                                                        + lower_left_corner_color[2] + lower_right_corner_color[2]) / 4

        cropped_target_image_average_corner_color = (cropped_target_image_average_corner_color_x, cropped_target_image_average_corner_color_y, cropped_target_image_average_corner_color_z)

        return cropped_target_image_average_corner_color

from PIL import Image

class BlobColorOperations(object):

    @staticmethod
    def find_blob_average_color(target_map_image, blob_location):
        """
        Find the average color of a blob by taking the average RGB value of
        nine uniformly separated pixels within this blob and return this average
        RGB value as a color of 3-tuple.

        :param target_map_image: the image of the background
        :param blob_location: the information of a single blob

        :type target_map_image: PIL image
        :type blob_location: a list containing four elements for each
                             blob: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        pixel_access_target_map_image = target_map_image.load()

        center_color = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] / 2)]

        upper_color_1 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] / 6)]
        upper_color_2 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] / 3)]

        lower_color_1 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] / 6 * 5)]
        lower_color_2 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] / 3 * 2)]

        left_color_1 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6), blob_location[1] + (blob_location[3] / 2)]
        left_color_2 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3), blob_location[1] + (blob_location[3] / 2)]

        right_color_1 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6 * 5), blob_location[1] + (blob_location[3] / 2)]
        right_color_2 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3 * 2), blob_location[1] + (blob_location[3] / 2)]

        left_upper_color_1 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6), blob_location[1] + (blob_location[3] / 6)]
        left_upper_color_2 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3), blob_location[1] + (blob_location[3] / 6)]
        left_upper_color_3 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6), blob_location[1] + (blob_location[3] / 3)]
        left_upper_color_4 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3), blob_location[1] + (blob_location[3] / 3)]

        right_upper_color_1 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3 * 2), blob_location[1] + (blob_location[3] / 6)]
        right_upper_color_2 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6 * 5), blob_location[1] + (blob_location[3] / 6)]
        right_upper_color_3 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3 * 2), blob_location[1] + (blob_location[3] / 3)]
        right_upper_color_4 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6 * 5), blob_location[1] + (blob_location[3] / 3)]

        left_lower_color_1 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6), blob_location[1] + (blob_location[3] / 3 * 2)]
        left_lower_color_2 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3), blob_location[1] + (blob_location[3] / 3 * 2)]
        left_lower_color_3 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6), blob_location[1] + (blob_location[3] / 6 * 5)]
        left_lower_color_4 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3), blob_location[1] + (blob_location[3] / 6 * 5)]

        right_lower_color_1 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3 * 2), blob_location[1] + (blob_location[3] / 3 * 2)]
        right_lower_color_2 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6 * 5), blob_location[1] + (blob_location[3] / 3 * 2)]
        right_lower_color_3 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 3 * 2), blob_location[1] + (blob_location[3] / 6 * 5)]
        right_lower_color_4 = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 6 * 5), blob_location[1] + (blob_location[3] / 6 * 5)]

        average_blob_color_x = (center_color[0] + upper_color_1[0] + upper_color_2[0] + lower_color_1[0] + lower_color_2[0] + left_color_1[0] + left_color_2[0] + right_color_1[0] + right_color_2[0]\
                                + left_upper_color_1[0] + left_upper_color_2[0] + left_upper_color_3[0] + left_upper_color_4[0] + right_upper_color_1[0] + right_upper_color_2[0] + right_upper_color_3[0] + right_upper_color_4[0]\
                                + left_lower_color_1[0] + left_lower_color_2[0] + left_lower_color_3[0] + left_lower_color_4[0] + right_lower_color_1[0] + right_lower_color_2[0] + right_lower_color_3[0] + right_lower_color_4[0]) / 25

        average_blob_color_y = (center_color[1] + upper_color_1[1] + upper_color_2[1] + lower_color_1[1] + lower_color_2[1] + left_color_1[1] + left_color_2[1] + right_color_1[1] + right_color_2[1]\
                                + left_upper_color_1[1] + left_upper_color_2[1] + left_upper_color_3[1] + left_upper_color_4[1] + right_upper_color_1[1] + right_upper_color_2[1] + right_upper_color_3[1] + right_upper_color_4[1]\
                                + left_lower_color_1[1] + left_lower_color_2[1] + left_lower_color_3[1] + left_lower_color_4[1] + right_lower_color_1[1] + right_lower_color_2[1] + right_lower_color_3[1] + right_lower_color_4[1]) / 25

        average_blob_color_z = (center_color[2] + upper_color_1[2] + upper_color_2[2] + lower_color_1[2] + lower_color_2[2] + left_color_1[2] + left_color_2[2] + right_color_1[2] + right_color_2[2]\
                                + left_upper_color_1[2] + left_upper_color_2[2] + left_upper_color_3[2] + left_upper_color_4[2] + right_upper_color_1[2] + right_upper_color_2[2] + right_upper_color_3[2] + right_upper_color_4[2]\
                                + left_lower_color_1[2] + left_lower_color_2[2] + left_lower_color_3[2] + left_lower_color_4[2] + right_lower_color_1[2] + right_lower_color_2[2] + right_lower_color_3[2] + right_lower_color_4[2]) / 25

        average_blob_color = (average_blob_color_x, average_blob_color_y, average_blob_color_z)

        return average_blob_color

    @staticmethod
    def find_surrounding_average_color(target_map_image, blob_location):
        """
        Find the average color of the surrounding color of a blob by taking the
        average RGB value of eight uniformly separated pixels around this blob
        and return this average RGB value as a color of 3-tuple.

        :param target_map_image: the image of the background
        :param blob_location: the information of a single blob

        :type target_map_image: PIL image
        :type blob_location: a list containing four elements for each
                             blob: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        left_x = blob_location[0] - (blob_location[2] / 4)
        right_x = blob_location[0] + blob_location[2] + (blob_location[2] / 4)
        upper_y = blob_location[1] - (blob_location[3] / 4)
        lower_y = blob_location[1] + blob_location[3] + (blob_location[3] / 4)

        if (left_x < 0):
            left_x = 0

        if (right_x >= target_map_image.width):
            right_x = target_map_image.width - 1

        if (upper_y < 0):
            upper_y = 0

        if (lower_y >= target_map_image.height):
            lower_y = target_map_image.height - 1

        pixel_access_target_map_image = target_map_image.load()

        upper_color = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 2), upper_y]
        lower_color = pixel_access_target_map_image[blob_location[0] + (blob_location[2] / 2), lower_y]
        left_color = pixel_access_target_map_image[left_x, blob_location[1] + (blob_location[3] / 2)]
        right_color = pixel_access_target_map_image[right_x, blob_location[1] + (blob_location[3] / 2)]

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
    def find_average_corner_color(cropped_blob_image):
        pixel_access_cropped_blob_image = cropped_blob_image.load()

        upper_left_corner_color = pixel_access_cropped_blob_image[1, 1]
        upper_right_corner_color = pixel_access_cropped_blob_image[cropped_blob_image.width - 2, 1]
        lower_left_corner_color = pixel_access_cropped_blob_image[1, cropped_blob_image.height - 2]
        lower_right_corner_color = pixel_access_cropped_blob_image[cropped_blob_image.width - 2, cropped_blob_image.height - 2]

        cropped_blob_image_average_corner_color_x = (upper_left_corner_color[0] + upper_right_corner_color[0]\
                                                        + lower_left_corner_color[0] + lower_right_corner_color[0]) / 4

        cropped_blob_image_average_corner_color_y = (upper_left_corner_color[1] + upper_right_corner_color[1]\
                                                        + lower_left_corner_color[1] + lower_right_corner_color[1]) / 4

        cropped_blob_image_average_corner_color_z = (upper_left_corner_color[2] + upper_right_corner_color[2]\
                                                        + lower_left_corner_color[2] + lower_right_corner_color[2]) / 4

        cropped_blob_image_average_corner_color = (cropped_blob_image_average_corner_color_x, cropped_blob_image_average_corner_color_y, cropped_blob_image_average_corner_color_z)

        return cropped_blob_image_average_corner_color

from PIL import Image

class BlobColorOperations(object):

    @staticmethod
    def find_blob_average_color(map_image, blob_location):
        """
        Find the average color of a blob by taking the average RGB value of
        nine uniformly separated pixels within this blob and return this average
        RGB value as a color of 3-tuple.

        :param map_image: the image of the background
        :param blob_location: the information of a single blob

        :type map_image: PIL image
        :type blob_location: a list containing four elements for each
                             blob: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        center_color = map_image.load()[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] / 2)]
        upper_color = map_image.load()[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] * 0.375)]
        lower_color = map_image.load()[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] * 0.625)]
        left_color = map_image.load()[blob_location[0] + (blob_location[2] * 0.375), blob_location[1] + (blob_location[3] / 2)]
        right_color = map_image.load()[blob_location[0] + (blob_location[2] * 0.625), blob_location[1] + (blob_location[3] / 2)]
        left_upper_color = map_image.load()[blob_location[0] + (blob_location[2] * 0.375), blob_location[1] + (blob_location[3] * 0.375)]
        right_upper_color = map_image.load()[blob_location[0] + (blob_location[2] * 0.625), blob_location[1] + (blob_location[3] * 0.375)]
        left_lower_color = map_image.load()[blob_location[0] + (blob_location[2] * 0.375), blob_location[1] + (blob_location[3] * 0.625)]
        right_lower_color = map_image.load()[blob_location[0] + (blob_location[2] * 0.625), blob_location[1] + (blob_location[3] * 0.625)]

        average_blob_color_x = (center_color[0] + upper_color[0] + lower_color[0] + left_color[0] + right_color[0] + left_upper_color[0] + right_upper_color[0] + left_lower_color[0] + right_lower_color[0]) / 9
        average_blob_color_y = (center_color[1] + upper_color[1] + lower_color[1] + left_color[1] + right_color[1] + left_upper_color[1] + right_upper_color[1] + left_lower_color[1] + right_lower_color[1]) / 9
        average_blob_color_z = (center_color[2] + upper_color[2] + lower_color[2] + left_color[2] + right_color[2] + left_upper_color[2] + right_upper_color[2] + left_lower_color[2] + right_lower_color[2]) / 9
        average_blob_color = (average_blob_color_x, average_blob_color_y, average_blob_color_z)

        return average_blob_color

    @staticmethod
    def find_surrounding_average_color(map_image, blob_location):
        """
        Find the average color of the surrounding color of a blob by taking the
        average RGB value of eight uniformly separated pixels around this blob
        and return this average RGB value as a color of 3-tuple.

        :param map_image: the image of the background
        :param blob_location: the information of a single blob

        :type map_image: PIL image
        :type blob_location: a list containing four elements for each
                             blob: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        upper_color = map_image.load()[blob_location[0] + (blob_location[2] / 2), blob_location[1] + (blob_location[3] / 5)]
        lower_color = map_image.load()[blob_location[0] + (blob_location[2] / 2), blob_location[1] + blob_location[3] - (blob_location[3] / 5)]
        left_color = map_image.load()[blob_location[0] + (blob_location[2] / 5), blob_location[1] + (blob_location[3] / 2)]
        right_color = map_image.load()[blob_location[0] + blob_location[2] - (blob_location[2] / 5), blob_location[1] + (blob_location[3] / 2)]

        left_upper_color = map_image.load()[blob_location[0] + (blob_location[2] / 4), blob_location[1] + (blob_location[3] / 4)]
        right_upper_color = map_image.load()[blob_location[0] + (blob_location[2] * 3 / 4), blob_location[1] + (blob_location[3] / 4)]
        left_lower_color = map_image.load()[blob_location[0] + (blob_location[2] / 4), blob_location[1] + (blob_location[3] * 3 / 4)]
        right_lower_color = map_image.load()[blob_location[0] + (blob_location[2] * 3 / 4), blob_location[1] + (blob_location[3] * 3 / 4)]

        average_surrounding_color_x = (upper_color[0] + lower_color[0] + left_color[0] + right_color[0] + left_upper_color[0] + right_upper_color[0] + left_lower_color[0] + right_lower_color[0]) / 8
        average_surrounding_color_y = (upper_color[1] + lower_color[1] + left_color[1] + right_color[1] + left_upper_color[1] + right_upper_color[1] + left_lower_color[1] + right_lower_color[1]) / 8
        average_surrounding_color_z = (upper_color[2] + lower_color[2] + left_color[2] + right_color[2] + left_upper_color[2] + right_upper_color[2] + left_lower_color[2] + right_lower_color[2]) / 8
        average_surrounding_color = (average_surrounding_color_x, average_surrounding_color_y, average_surrounding_color_z)

        return average_surrounding_color

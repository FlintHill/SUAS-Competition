import math
from PIL import Image
from .color_operations import ColorOperations

class FalsePositiveEliminator(object):

    @staticmethod
    def eliminate_overrepeated_colors(image_path, positive_list):
        """
        Eliminate false positives after blob detection.

        :param image_path: the path of an image
        :param positive_list: the list holding the information of the blobs.

        :type image_path: an image file such as JPG and PNG
        :type positive_list: a list of lists containing four elements for each
                             blob: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int

        Concept:
        Find the average color of all the blobs. Compare that color to the color
        of each blob. Save all the blobs with colors that stand out from the
        rest and eliminate the rest.

        (The colors of the targets differ from the colors of the background. By
        eliminating the blobs of the background, targets remain)

        Procedure:
        1. Create blob_color_list for containing the colors of all blobs.
        2. For each blob, find the average RGB values of nine uniformly separated
           pixels and save these average RGB values as colors of 3-tuples into
           blob_color_list.
        3. Find the average RGB value of all RGB values saved in
           blob_color_list.
        4. Using the find_percentage_difference method in ColorOperations to
           find the percentage_difference between each RGB value in
           blob_color_list and the average RGB value of all blob colors.
        5. Set a threshold of percentage_difference to eliminate the blobs.
        """

        blob_color_list = []
        image = Image.open(image_path)
        for index in range(len(positive_list)):
            center_color = image.load()[positive_list[index][0] + (positive_list[index][2] / 2), positive_list[index][1] + (positive_list[index][3] / 2)]
            upper_color = image.load()[positive_list[index][0] + (positive_list[index][2] / 2), positive_list[index][1] + (positive_list[index][3] * 0.375)]
            lower_color = image.load()[positive_list[index][0] + (positive_list[index][2] / 2), positive_list[index][1] + (positive_list[index][3] * 0.625)]
            left_color = image.load()[positive_list[index][0] + (positive_list[index][2] * 0.375), positive_list[index][1] + (positive_list[index][3] / 2)]
            right_color = image.load()[positive_list[index][0] + (positive_list[index][2] * 0.625), positive_list[index][1] + (positive_list[index][3] / 2)]
            left_upper_color = image.load()[positive_list[index][0] + (positive_list[index][2] * 0.375), positive_list[index][1] + (positive_list[index][3] * 0.375)]
            right_upper_color = image.load()[positive_list[index][0] + (positive_list[index][2] * 0.625), positive_list[index][1] + (positive_list[index][3] * 0.375)]
            left_lower_color = image.load()[positive_list[index][0] + (positive_list[index][2] * 0.375), positive_list[index][1] + (positive_list[index][3] * 0.625)]
            right_lower_color = image.load()[positive_list[index][0] + (positive_list[index][2] * 0.625), positive_list[index][1] + (positive_list[index][3] * 0.625)]

            average_blob_color_x = (center_color[0] + upper_color[0] + lower_color[0] + left_color[0] + right_color[0] + left_upper_color[0] + right_upper_color[0] + left_lower_color[0] + right_lower_color[0]) / 9
            average_blob_color_y = (center_color[1] + upper_color[1] + lower_color[1] + left_color[1] + right_color[1] + left_upper_color[1] + right_upper_color[1] + left_lower_color[1] + right_lower_color[1]) / 9
            average_blob_color_z = (center_color[2] + upper_color[2] + lower_color[2] + left_color[2] + right_color[2] + left_upper_color[2] + right_upper_color[2] + left_lower_color[2] + right_lower_color[2]) / 9
            average_blob_color = (average_blob_color_x, average_blob_color_y, average_blob_color_z)

            blob_color_list.append(average_blob_color)

        average_list_color_x = 0
        average_list_color_y = 0
        average_list_color_z = 0

        for index in range(len(blob_color_list)):
            average_list_color_x += blob_color_list[index][0]
            average_list_color_y += blob_color_list[index][1]
            average_list_color_z += blob_color_list[index][2]

        average_list_color = (average_list_color_x / len(blob_color_list) , average_list_color_y / len(blob_color_list), average_list_color_z / len(blob_color_list))

        remaining_blob_list = []
        index = len(positive_list) - 1
        while (index >= 0):
            percentage_difference = ColorOperations.find_percentage_difference(average_list_color, blob_color_list[index])

            if (percentage_difference >= 15):
                remaining_blob_list.append(positive_list[index])

            index -= 1

        return remaining_blob_list

    @staticmethod
    def eliminate_overlapping_blobs(positive_list):
        """
        Eliminate overlapping blobs after blob detection.

        :param positive_list: the list holding the information of the blobs.

        :type positive_list: a list of lists containing four elements for each
                             blob: [x, y, length, width]
        :type x: int
        :type y: int
        :type length: int
        :type width: int

        Concept:
        Using the information of blobs given by positive_list, Compare the
        centers of each blob with every other blob in the list. If the x
        distance and y distance are both smaller than the diameter of the larger
        blob in comparison, eliminate the smaller blob.
        """

        list_to_eliminate = []
        for index_1 in range(len(positive_list)):
            for index_2 in range(index_1 + 1, len(positive_list)):
                target_1_center_x = positive_list[index_1][0] + (0.5 * positive_list[index_1][2])
                target_1_center_y = positive_list[index_1][1] + (0.5 * positive_list[index_1][3])
                target_2_center_x = positive_list[index_2][0] + (0.5 * positive_list[index_2][2])
                target_2_center_y = positive_list[index_2][1] + (0.5 * positive_list[index_2][3])

                x_distance = abs(target_1_center_x - target_2_center_x)
                y_distance = abs(target_1_center_y - target_2_center_y)

                larger_x = positive_list[index_1][2] / 2
                larger_y = positive_list[index_1][3] / 2
                smaller_x = positive_list[index_2][2] / 2
                smaller_y = positive_list[index_2][3] / 2
                index_of_potential_blob_to_eliminate = index_2

                if (positive_list[index_1][2] < positive_list[index_2][2]):
                    larger_x = positive_list[index_2][2] / 2
                    smaller_x = positive_list[index_1][2] / 2
                    index_of_potential_blob_to_eliminate = index_1

                if (positive_list[index_1][3] < positive_list[index_2][3]):
                    larger_y = positive_list[index_2][3] / 2
                    smaller_y = positive_list[index_1][3] / 2
                    index_of_potential_blob_to_eliminate = index_1

                if ((x_distance < (larger_x + smaller_x)) and (y_distance < (larger_y + smaller_y))):
                    list_to_eliminate.append(index_of_potential_blob_to_eliminate)

        list_to_eliminate = list(set(list_to_eliminate))
        list_to_eliminate.sort()

        index = len(list_to_eliminate) - 1
        while (index >= 0):
            positive_list.pop(list_to_eliminate[index])
            index -= 1

        return positive_list

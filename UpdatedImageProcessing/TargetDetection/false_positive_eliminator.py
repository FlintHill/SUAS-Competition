from PIL import Image
from .color_operations import ColorOperations
from .blob_color_operations import BlobColorOperations

class FalsePositiveEliminator(object):

    @staticmethod
    def eliminate_overrepeated_colors(image_path, positive_list):
        """
        Eliminate false positives after blob detection.

        (This method works better when there are significantly more false
        positives than real targets)

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
        rest and eliminate the rest. The colors of the targets differ from the
        colors of the background. By eliminating the blobs of the background,
        targets remain.
        """
        image = Image.open(image_path)
        blob_color_list = []
        for index in range(len(positive_list)):
            average_blob_color = BlobColorOperations.find_blob_average_color(image, positive_list[index])
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
        Compare the centers of each blob with every other blob in positive_list.
        If the x distance and y distance between two blobs are both smaller than
        the combination of the diameters of the larger blob and the smaller
        blob, eliminate the smaller blob.
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

    @staticmethod
    def eliminate_by_surrounding_color(image_path, positive_list):
        """
        Eliminate false positives after blob detection.

        (This method works better when there are less number of false positives.
        If this condition does not apply, use eliminate_overrepeated_colors
        first to ensure better results.)

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
        For every blob given by positive_list, if its surrounding color is below
        a certain threshold, eliminate this blob. The targets have colors that
        stand out from the background, if a blob's color conforms with the
        background color, then it is not a target.
        """
        image = Image.open(image_path)
        list_to_eliminate = []
        for index in range(len(positive_list)):
            average_surrounding_color = BlobColorOperations.find_surrounding_average_color(image, positive_list[index])
            average_blob_color = BlobColorOperations.find_blob_average_color(image, positive_list[index])

            percentage_difference = ColorOperations.find_percentage_difference(average_surrounding_color, average_blob_color)
            if (percentage_difference <= 10):
                list_to_eliminate.append(index)

        list_to_eliminate = list(set(list_to_eliminate))
        list_to_eliminate.sort()

        index = len(list_to_eliminate) - 1
        while (index >= 0):
            positive_list.pop(list_to_eliminate[index])
            index -= 1

        return positive_list

from PIL import Image
from .settings import Settings
from .color_operations import ColorOperations
from .target_analyzer import TargetAnalyzer

class FalsePositiveEliminators(object):

    @staticmethod
    def eliminate_overrepeated_colors(target_map_image, positive_list):
        """
        Eliminate false positives after target detection.

        (This method works better when there are significantly more false
        positives than real targets)

        :param target_map_image: the image of the background
        :param positive_list: the list holding the information of the targets.

        :type target_map_image: PIL image
        :type positive_list: a list of four-tuples containing four elements for each
                             target: (x, y, length, width)
        :type x: int
        :type y: int
        :type length: int
        :type width: int

        Concept:
        Find the average color of all the targets. Compare that color to the color
        of each target. Save all the targets with colors that stand out from the
        rest and eliminate the rest. The colors of the targets differ from the
        colors of the background. By eliminating the targets of the background,
        targets remain.
        """
        target_color_list = []
        for index in range(len(positive_list)):
            average_target_color = TargetAnalyzer.find_target_average_color(target_map_image, positive_list[index])
            target_color_list.append(average_target_color)

        average_list_color_x = 0
        average_list_color_y = 0
        average_list_color_z = 0

        for index in range(len(target_color_list)):
            average_list_color_x += target_color_list[index][0]
            average_list_color_y += target_color_list[index][1]
            average_list_color_z += target_color_list[index][2]

        average_list_color = (average_list_color_x / len(target_color_list) , average_list_color_y / len(target_color_list), average_list_color_z / len(target_color_list))

        remaining_target_list = []
        index = len(positive_list) - 1
        while (index >= 0):
            percentage_difference = ColorOperations.find_percentage_difference(average_list_color, target_color_list[index])

            if (percentage_difference >= 15):
                remaining_target_list.append(positive_list[index])

            index -= 1

        return remaining_target_list

    @staticmethod
    def eliminate_by_surrounding_color(target_map_image, positive_list):
        """
        Eliminate false positives after target detection.

        (This method works better when there are less number of false positives.
        If this condition does not apply, use eliminate_overrepeated_colors
        first to ensure better results.)

        :param target_map_image: the image of the background
        :param positive_list: the list holding the information of the targets.

        :type target_map_image: PIL image
        :type positive_list: a list of four-tuples containing four elements for each
                             target: (x, y, length, width)
        :type x: int
        :type y: int
        :type length: int
        :type width: int

        Concept:
        For every target given by positive_list, if its surrounding color is below
        a certain threshold, eliminate this target. The targets have colors that
        stand out from the background, if a target's color conforms with the
        background color, then it is not a target.
        """
        list_to_eliminate = []
        for index in range(len(positive_list)):
            average_surrounding_color = TargetAnalyzer.find_surrounding_average_color(target_map_image, positive_list[index])
            average_target_color = TargetAnalyzer.find_target_average_color(target_map_image, positive_list[index])

            percentage_difference = ColorOperations.find_percentage_difference(average_surrounding_color, average_target_color)
            if (percentage_difference <= 10):
                list_to_eliminate.append(index)

        list_to_eliminate = list(set(list_to_eliminate))
        list_to_eliminate.sort()

        index = len(list_to_eliminate) - 1
        while (index >= 0):
            positive_list.pop(list_to_eliminate[index])
            index -= 1

        return positive_list

    @staticmethod
    def combine_close_by_targets(positive_list):
        """
        :param positive_list: the list holding the information of the targets.

        :type positive_list: a list of four-tuples containing four elements for each
                             target: (x, y, length, width)
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        close_by_targets = []
        list_to_append = []

        for index_1 in range(len(positive_list)):
            for index_2 in range(index_1 + 1, len(positive_list)):

                if ((positive_list[index_1] == -1) or (positive_list[index_2] == -1)):
                    continue

                target_1_center_x = positive_list[index_1][0] + (positive_list[index_1][2] / 2)
                target_1_center_y = positive_list[index_1][1] + (positive_list[index_1][3] / 2)
                target_2_center_x = positive_list[index_2][0] + (positive_list[index_2][2] / 2)
                target_2_center_y = positive_list[index_2][1] + (positive_list[index_2][3] / 2)

                x_distance = abs(target_1_center_x - target_2_center_x)
                y_distance = abs(target_1_center_y - target_2_center_y)

                target_1_radius = positive_list[index_1][2]
                target_2_radius = positive_list[index_2][2]

                if ((x_distance < ((target_1_radius + target_2_radius) * 1.5)) and (y_distance < ((target_1_radius + target_2_radius) * 1.5))):
                    close_by_targets.append([positive_list[index_1], positive_list[index_2]])
                    positive_list[index_1] = -1
                    positive_list[index_2] = -1

        for index in range(len(close_by_targets)):
            target_1_x = close_by_targets[index][0][0]
            target_1_y = close_by_targets[index][0][1]
            target_1_width = close_by_targets[index][0][2]
            target_1_height = close_by_targets[index][0][3]

            target_2_x = close_by_targets[index][1][0]
            target_2_y = close_by_targets[index][1][1]
            target_2_width = close_by_targets[index][1][2]
            target_2_height = close_by_targets[index][1][3]

            average_x = (target_1_x + target_2_x) / 2
            average_y = (target_1_y + target_2_y) / 2
            average_width = (target_1_width + target_2_width) / 2
            average_height = (target_1_height + target_2_height) / 2

            list_to_append.append((average_x, average_y, average_width, average_height))

        index = len(positive_list) - 1
        while (index >= 0):
            if (positive_list[index] == -1):
                positive_list.pop(index)
            index -= 1

        for index in range(len(list_to_append)):
            positive_list.append(list_to_append[index])

        number_of_close_by_targets = len(close_by_targets)

        return [positive_list, number_of_close_by_targets]

    @staticmethod
    def eliminate_overlapping_targets(positive_list):
        """
        :param positive_list: the list holding the information of the targets.

        :type positive_list: a list of four-tuples containing four elements for each
                             target: (x, y, length, width)
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        for index_1 in range(len(positive_list)):
            for index_2 in range(index_1 + 1, len(positive_list)):

                if ((positive_list[index_1] == -1) or (positive_list[index_2] == -1)):
                    continue

                target_1_center_x = positive_list[index_1][0] + (positive_list[index_1][2] / 2)
                target_1_center_y = positive_list[index_1][1] + (positive_list[index_1][3] / 2)
                target_2_center_x = positive_list[index_2][0] + (positive_list[index_2][2] / 2)
                target_2_center_y = positive_list[index_2][1] + (positive_list[index_2][3] / 2)

                x_distance = abs(target_1_center_x - target_2_center_x)
                y_distance = abs(target_1_center_y - target_2_center_y)

                target_1_radius = positive_list[index_1][2]
                target_2_radius = positive_list[index_2][2]

                if ((x_distance < (target_1_radius + target_2_radius)) and (y_distance < (target_1_radius + target_2_radius))):
                    if ((positive_list[index_1][2] + positive_list[index_1][3]) > (positive_list[index_2][2] + positive_list[index_2][3])):
                        positive_list[index_2] = -1
                    else:
                        positive_list[index_1] = -1

        new_positive_list = []
        for index_3 in range(len(positive_list)):
            if (positive_list[index_3] != -1):
                new_positive_list.append(positive_list[index_3])

        return new_positive_list

    @staticmethod
    def eliminate_target_not_on_grass(target_image):
        average_rim_color = TargetAnalyzer.find_rim_average_color(target_image)
        color_difference = ColorOperations.find_percentage_difference(average_rim_color, Settings.GRASS_COLOR)
        if (color_difference > 10):
            return 0
        else:
            return 1

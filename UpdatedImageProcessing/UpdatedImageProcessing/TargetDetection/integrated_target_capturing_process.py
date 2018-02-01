from PIL import Image
from PIL import ImageFilter
from collections import Counter
from .color_operations import ColorOperations
from .target_analyzer import TargetAnalyzer
from .false_positive_eliminators import FalsePositiveEliminators
from .background_color_nullifier import BackgroundColorNullifier

class IntegratedTargetCapturingProcess(object):

    @staticmethod
    def run_integrated_target_capturing_process(target_map_image_path, positive_list):
        """
        Crop the single targets with information given by target_location.

        :param target_map_image_path: the path to the target map image
        :param positive_list: the list holding information of the locations of
                              targets, which are four-tuples of the target's top
                              left x, top left y, width, and height

        :type target_map_image_path: an image file such as JPG and PNG
        :type positive_list: list
        :type target_location: (x, y, width, height)
        :type x: int
        :type y: int
        :type length: int
        :type width: int

        Concept:
        Stage 1
        Find the average color of the target_map.

        Stage 2
        For every detected target on the target map:
        1. Crop it out with 30-pixel margins on each side.
        2. Find the average_corner_color of the image.
        3. Find the rim_average_color of the image.

        if the average_corner_color is not within 15 percent difference from the
        rim_average_color, the target is determined as a false positive and is
        added to list_to_eliminate.
        Otherwise, proceed to to Stage 3.

        Stage 3
        Apply BackgroundColorNullifier.nullify_color_and_recrop_target to the
        image. For more detail see .background_color_nullifier.
        """
        target_map_image = Image.open(target_map_image_path)
        target_map_image_average_color = TargetAnalyzer.find_target_average_color(target_map_image, (0, 0, target_map_image.width, target_map_image.height))

        resultant_image_list = []
        list_to_eliminate = []
        for index in range(len(positive_list)):

            target_location = positive_list[index]

            target_x = target_location[0]
            target_y = target_location[1]
            target_width = target_location[2]
            target_height = target_location[3]

            crop_x1 = target_x - 30
            crop_y1 = target_y - 30
            crop_x2 = target_x + target_width + 30
            crop_y2 = target_y + target_height + 30

            if (crop_x1 < 0):
                crop_x1 = 0

            if (crop_x2 >= target_map_image.width):
                crop_x2 = target_map_image.width - 1

            if (crop_y1 < 0):
                crop_y1 = 0

            if (crop_y2 >= target_map_image.height):
                crop_y2 = target_map_image.height - 1

            captured_image = target_map_image.crop((crop_x1, crop_y1, crop_x2, crop_y2))

            '''
            if (FalsePositiveEliminators.eliminate_target_not_on_grass(captured_image) == 0):
                list_to_eliminate.append(index)
                continue
            '''
            
            captured_image_average_corner_color = TargetAnalyzer.find_average_corner_color(captured_image)
            captured_image_rim_average_color = TargetAnalyzer.find_rim_average_color(captured_image)
            percentage_difference = ColorOperations.find_percentage_difference(captured_image_average_corner_color, captured_image_rim_average_color)

            if (percentage_difference > 15):
                list_to_eliminate.append(index)
                continue

            else:
                color_nullifying_result = BackgroundColorNullifier.nullify_color_and_recrop_target(captured_image, 10)
                if (color_nullifying_result == 0):
                    list_to_eliminate.append(index)
                else:
                    resultant_image_list.append(color_nullifying_result)

        return [resultant_image_list, list_to_eliminate]

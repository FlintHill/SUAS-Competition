from PIL import Image
from PIL import ImageFilter
from collections import Counter
from .color_operations import ColorOperations
from .blob_color_operations import BlobColorOperations

class SingleTargetsCapturer(object):

    @staticmethod
    def capture_single_targets(target_map_path, positive_list):
        """
        Using color quantization, crop the single targets with information given
        by blob_location.

        :param target_map_path: the path to the target map image
        :param blob_location: a four-tuple of the blob's top left x, top left y,
                              width, and height

        :type target_map_path: an image file such as JPG and PNG
        :type blob_location: (x, y, width, height)
        :type x: int
        :type y: int
        :type length: int
        :type width: int
        """
        target_map = Image.open(target_map_path)
        target_map_average_color = BlobColorOperations.find_blob_average_color(target_map, (0, 0, target_map.width, target_map.height))

        resultant_image_list = []
        list_to_eliminate = []
        for index in range(len(positive_list)):


            blob_location = positive_list[index]

            blob_x = blob_location[0]
            blob_y = blob_location[1]
            blob_width = blob_location[2]
            blob_height = blob_location[3]

            crop_x1 = blob_x - 10
            crop_y1 = blob_y - 10
            crop_x2 = blob_x + blob_width + 10
            crop_y2 = blob_y + blob_height + 10

            if (crop_x1 < 0):
                crop_x1 = 0

            if (crop_x2 >= target_map.width):
                crop_x2 = target_map.width - 1

            if (crop_y1 < 0):
                crop_y1 = 0

            if (crop_y2 >= target_map.height):
                crop_y2 = target_map.height - 1

            captured_image = target_map.crop((crop_x1, crop_y1, crop_x2, crop_y2))
            quantized_image = ColorOperations.quantize_color(captured_image, 3)
            quantized_image_average_corner_color = BlobColorOperations.find_average_corner_color(quantized_image)

            percentage_difference = ColorOperations.find_percentage_difference(target_map_average_color, quantized_image_average_corner_color)

            if (percentage_difference >= 5):

                crop_x1 = blob_x - (blob_width * 2)
                crop_y1 = blob_y - (blob_height * 2)
                crop_x2 = blob_x + (blob_width * 3)
                crop_y2 = blob_y + (blob_height * 3)

                if (crop_x1 < 0):
                    crop_x1 = 0

                if (crop_x2 >= target_map.width):
                    crop_x2 = target_map.width - 1

                if (crop_y1 < 0):
                    crop_y1 = 0

                if (crop_y2 >= target_map.height):
                    crop_y2 = target_map.height - 1

                captured_image = target_map.crop((crop_x1, crop_y1, crop_x2, crop_y2))
                quantized_image = ColorOperations.quantize_color(captured_image, 3)

                average_corner_color = BlobColorOperations.find_average_corner_color(quantized_image)

                target_color = (0, 0, 0, 0)
                target_found = False
                for x in range(quantized_image.width):
                    for y in range(1, quantized_image.height):
                        percentage_difference = ColorOperations.find_percentage_difference(average_corner_color, quantized_image.load()[x, y])
                        if ((percentage_difference >= 15) and (quantized_image.load()[x, y] == quantized_image.load()[x, y - 1])):
                            target_color = quantized_image.load()[x, y]
                            target_found = True
                            break

                if (target_found == False):
                    list_to_eliminate.append(index)
                    continue

                target_boundary = ColorOperations.find_boundary_of_color(quantized_image, target_color)

                crop_x1 = target_boundary[0] - 10
                crop_y1 = target_boundary[1] - 10
                crop_x2 = target_boundary[2] + 10
                crop_y2 = target_boundary[3] + 10

                if (crop_x1 < 0):
                    crop_x1 = 0

                if (crop_x2 >= quantized_image.width):
                    crop_x2 = quantized_image.width - 1

                if (crop_y1 < 0):
                    crop_y1 = 0

                if (crop_y2 >= quantized_image.height):
                    crop_y2 = quantized_image.height - 1

                captured_image = captured_image.crop((crop_x1, crop_y1, crop_x2, crop_y2))
                quantized_image = quantized_image.crop((crop_x1, crop_y1, crop_x2, crop_y2))

            list_of_colors = []
            for x in range(quantized_image.width):
                for y in range(quantized_image.height):
                    list_of_colors.append(quantized_image.load()[x, y])

            list_of_most_common_colors = Counter(list_of_colors).most_common(2)

            if ((quantized_image.load()[1, 1] == list_of_most_common_colors[0][0]) or (quantized_image.load()[quantized_image.width - 1, quantized_image.height - 1] == list_of_most_common_colors[0][0])):
                background_color = list_of_most_common_colors[0][0]
                shape_color = list_of_most_common_colors[1][0]
            else:
                background_color = list_of_most_common_colors[1][0]
                shape_color = list_of_most_common_colors[0][0]

            shape_color_boundary = ColorOperations.find_boundary_of_color(quantized_image, shape_color)
            captured_image_with_background_nullified = ColorOperations.nullify_color(captured_image, quantized_image, background_color)

            resultant_image = captured_image_with_background_nullified.crop(shape_color_boundary)
            resultant_image_list.append(resultant_image)

        return [resultant_image_list, list_to_eliminate]

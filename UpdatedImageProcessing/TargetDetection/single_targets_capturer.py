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

        Concept:

        Stage 1
        Find the average color of the target_map.

        Stage 2
        For every detected target on the target map:
        1. Crop it out with 20-pixel margins on each side.
        2. Color quantize the cropped image.
        3. Find the average_corner_color of the quantized image.

        if the average_corner_color is within 10 percent difference from the
        average color of the target_map, the target is detected based on its
        shape; proceed to Stage 4.
        Otherwise, proceed to to Stage 3.

        Stage 4
        1. Find the border color(s) of the quantized image.
        2. If the border color is constant, then the three colors for the
           cropped image are: background_color_1, target_color, and
           letter_color. And background_color_2 is set to 0.

           If the border color is not constant, then the three colors for the
           cropped image are: background_color_1, background_color_2, and
           target_color with background_color_1 having more frequent appearance.
           The letter_color is either blended with the target_color or shares
           its color with one of the background_colors.
        3. Find the frequencies of the three colors' appearance on the image.
           If neither background_color_1 nor background_color_2 has the most
           frequent appearance, then the shape_color is set to the color with
           the most frequent appearance.

           If background_color_1 has the most frequent appearance and
           background_color_2 has the second most frequent appearance, then
           shape_color is set to the color with the least frequent appearance.

           If neither of the two cases above applies, then shape_color is set to
           the color with the second frequent appearance.
        4. With the knowledge of the shape_color, nullify the background_colors,
           namely, all the colors that lie outside of the shape's boundary.
        5. Recrop the image down to the shape's boundary with 5-pixel margins on
           each side.
        6. Append the resultant_image into the resultant_image_list.
        7. Return the resultant_image_list along with list_to_eliminate.
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

            crop_x1 = blob_x - 20
            crop_y1 = blob_y - 20
            crop_x2 = blob_x + blob_width + 20
            crop_y2 = blob_y + blob_height + 20

            if (crop_x1 < 0):
                crop_x1 = 0

            if (crop_x2 >= target_map.width):
                crop_x2 = target_map.width - 1

            if (crop_y1 < 0):
                crop_y1 = 0

            if (crop_y2 >= target_map.height):
                crop_y2 = target_map.height - 1

            captured_image = target_map.crop((crop_x1, crop_y1, crop_x2, crop_y2))
            quantized_image = ColorOperations.quantize_color(captured_image, 4)
            quantized_image_average_corner_color = BlobColorOperations.find_average_corner_color(quantized_image)
            percentage_difference = ColorOperations.find_percentage_difference(target_map_average_color, quantized_image_average_corner_color)
            """
            if (percentage_difference >= 10):

                list_to_eliminate.append(index)
                continue
            """
            captured_image_with_background_nullified = ColorOperations.nullify_color_and_crop_to_target(captured_image, quantized_image, 15)
            resultant_image = captured_image_with_background_nullified
            resultant_image_list.append(resultant_image)

        return [resultant_image_list, list_to_eliminate]

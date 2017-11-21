from PIL import Image
from collections import Counter
from .color_operations import ColorOperations

class SingleTargetCapturer(object):

    @staticmethod
    def capture_single_target(target_map_path, blob_location):
        """

        """
        target_map = Image.open(target_map_path)
        captured_image = target_map.crop((blob_location[0], blob_location[1], blob_location[0] + blob_location[2], blob_location[1] + blob_location[3]))
        quantized_image = ColorOperations.quantize_color(captured_image, 2)

        list_of_colors = []
        for x in range(captured_image.width):
            for y in range(captured_image.height):
                list_of_colors.append(quantized_image.load()[x, y])

        list_of_most_common_colors = Counter(list_of_colors).most_common(2)
        background_color = list_of_most_common_colors[0][0]
        shape_color = list_of_most_common_colors[1][0]

        shape_color_boundary = ColorOperations.find_boundary_of_color(quantized_image, shape_color)

        captured_image_with_background_nullified = ColorOperations.nullify_color(captured_image, quantized_image, background_color)

        resultant_image = captured_image_with_background_nullified.crop(shape_color_boundary)
        resultant_image.show()

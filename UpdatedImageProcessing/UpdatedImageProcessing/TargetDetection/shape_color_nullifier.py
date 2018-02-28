from PIL import Image
from .color_operations import ColorOperations
from .target_analyzer import TargetAnalyzer
from .background_color_nullifier import BackgroundColorNullifier

class ShapeColorNullifier(object):

    @staticmethod
    def nullify_shape_color(captured_image, color_difference_threshold):
        """
        Scan through a captured_image, both line by line and column by column,
        starting from all four directions. During this process, if the current
        pixel under scanning is within the color_difference_threshold, this
        current pixel is set to transparent. Otherwise, the location of the
        current pixel is marked, and the color-nullifying process on this
        specific line or column from this specific direction is finished.

        :param captured_image: a captured image of a potential target
        :param color_difference_threshold: the threshold percentage difference
                                           between colors for determining
                                           the boundary of the target.
        :type captured_image: a PIL image
        :type color_difference_threshold: int

        :return: a PIL image
        """
        captured_image = captured_image.convert("RGBA")
        pixel_access_captured_image = captured_image.load()

        quantized_captured_image = ColorOperations.apply_color_quantization(captured_image, 3)
        quantized_captured_image = quantized_captured_image.convert("RGBA")
        pixel_access_quantized_captured_image = quantized_captured_image.load()
        rim_color = []

        for x in range(captured_image.width):
            for y in range(1, captured_image.height):
                if (pixel_access_captured_image[x, y][3] != 0):
                    if (pixel_access_captured_image[x, y + 5][3] != 0):
                        rim_color.append(pixel_access_quantized_captured_image[x, y + 5])
                        break

            y = captured_image.height - 1
            while (y >= 0):
                if (pixel_access_captured_image[x, y][3] != 0):
                    if (pixel_access_captured_image[x, y - 5][3] != 0):
                        rim_color.append(pixel_access_quantized_captured_image[x, y - 5])
                        break
                y -= 1

        for y in range(captured_image.height):
            for x in range(1, captured_image.width):
                if (pixel_access_captured_image[x, y][3] != 0):
                    if (pixel_access_captured_image[x + 5, y][3] != 0):
                        rim_color.append(pixel_access_quantized_captured_image[x + 5, y])
                        break

            x = captured_image.width - 1
            while (x >= 0):
                if (pixel_access_captured_image[x, y][3] != 0):
                    if (pixel_access_captured_image[x - 5, y][3] != 0):
                        rim_color.append(pixel_access_quantized_captured_image[x - 5, y])
                        break
                x -= 1

        threshold_color = max(set(rim_color), key=rim_color.count)

        print threshold_color
        for x in range(captured_image.width):
            for y in range(1, captured_image.height):
                if (pixel_access_captured_image[x, y][3] != 0):
                    color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_quantized_captured_image[x, y])
                    if (color_difference > color_difference_threshold):
                        break
                    else:
                        quantized_captured_image.putpixel((x, y), (255, 255, 255, 0))

            y = captured_image.height - 1
            while (y >= 0):
                if (pixel_access_captured_image[x, y][3] != 0):
                    color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_quantized_captured_image[x, y])

                    if (color_difference > color_difference_threshold):
                        break
                    else:
                        quantized_captured_image.putpixel((x, y), (255, 255, 255, 0))
                y -= 1

        for y in range(captured_image.height):
            for x in range(1, captured_image.width):
                if (pixel_access_captured_image[x, y][3] != 0):
                    color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_quantized_captured_image[x, y])

                    if (color_difference > color_difference_threshold):
                        break
                    else:
                        quantized_captured_image.putpixel((x, y), (255, 255, 255, 0))

            x = captured_image.width - 1
            while (x >= 0):
                if (pixel_access_captured_image[x, y][3] != 0):
                    color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_quantized_captured_image[x, y])

                    if (color_difference > color_difference_threshold):
                        break
                    else:
                        quantized_captured_image.putpixel((x, y), (255, 255, 255, 0))
                x -= 1

        captured_image.show()
        quantized_captured_image.show()

        recaptured_image = ShapeColorNullifier.recrop_target(quantized_captured_image)
        recaptured_image.show()

    @staticmethod
    def recrop_target(captured_image):
        """
        Scan through a captured_image, recapture the image so that 5-pixel
        margins from any non-transparent colors are left on all four directions.

        :param captured_image: a captured image of a potential target

        :type captured_image: a PIL image

        :return: a PIL image
        """
        pixel_access_captured_image = captured_image.load()
        stopping_x = []
        stopping_y = []
        is_false_void_color_present = False
        false_void_color = -1

        if (pixel_access_captured_image[1, 1][3] != 0):
             false_void_color = pixel_access_captured_image[1, 1]
             is_false_void_color_present = True

        if (pixel_access_captured_image[1, captured_image.height - 1][3] != 0):
             false_void_color = pixel_access_captured_image[1, captured_image.height - 1]
             is_false_void_color_present = True

        if (pixel_access_captured_image[captured_image.width - 1, 1][3] != 0):
             false_void_color = pixel_access_captured_image[captured_image.width - 1, 1]
             is_false_void_color_present = True

        if (pixel_access_captured_image[captured_image.width - 1, captured_image.height - 1][3] != 0):
             false_void_color = pixel_access_captured_image[captured_image.width - 1, captured_image.height - 1]
             is_false_void_color_present = True

        for x in range(captured_image.width):

            for y in range(1, captured_image.height):
                if (is_false_void_color_present == True):
                    if (pixel_access_captured_image[x, y] != false_void_color) and (pixel_access_captured_image[x, y][3] != 0):
                        stopping_y.append(y)
                        break
                else:
                    if (pixel_access_captured_image[x, y][3] != 0):
                        stopping_y.append(y)
                        break

            y = captured_image.height - 1
            while (y >= 0):
                if (is_false_void_color_present == True):
                    if (pixel_access_captured_image[x, y] != false_void_color) and (pixel_access_captured_image[x, y][3] != 0):
                        stopping_y.append(y)
                        break
                else:
                    if (pixel_access_captured_image[x, y][3] != 0):
                        stopping_y.append(y)
                        break
                y -= 1

        for y in range(captured_image.height):
            for x in range(1, captured_image.width):
                if (is_false_void_color_present == True):
                    if (pixel_access_captured_image[x, y] != false_void_color) and (pixel_access_captured_image[x, y][3] != 0):
                        stopping_x.append(x)
                        break
                else:
                    if (pixel_access_captured_image[x, y][3] != 0):
                        stopping_x.append(x)
                        break

            x = captured_image.width - 1
            while (x >= 0):
                if (is_false_void_color_present == True):
                    if (pixel_access_captured_image[x, y] != false_void_color) and (pixel_access_captured_image[x, y][3] != 0):
                        stopping_x.append(x)
                        break
                else:
                    if (pixel_access_captured_image[x, y][3] != 0):
                        stopping_x.append(x)
                        break
                x -= 1

        x_min = min(stopping_x)
        y_min = min(stopping_y)
        x_max = max(stopping_x)
        y_max = max(stopping_y)

        recaptured_image = captured_image.crop((x_min - 5, y_min - 5, x_max + 5, y_max + 5))
        return recaptured_image

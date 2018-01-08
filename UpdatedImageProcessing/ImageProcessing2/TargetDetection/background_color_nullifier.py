from .color_operations import ColorOperations
from .target_analyzer import TargetAnalyzer
from PIL import Image

class BackgroundColorNullifier(object):

    @staticmethod
    def nullify_color_and_recrop_target(captured_image, color_difference_threshold):
        """
        :param captured_image: a captured image of a potential target
        :param color_difference_threshold: the threshold percentage difference
                                           between colors for determining
                                           the boundary of the target.

        :type captured_image: an image file such as JPG and PNG
        :type color_difference_threshold: int
        """
        stopping_x = []
        stopping_y = []
        captured_image = captured_image.convert("RGBA")
        pixel_access_captured_image = captured_image.load()
        threshold_color = TargetAnalyzer.find_rim_average_color(captured_image)

        to_eliminate = False
        for x in range(captured_image.width):
            color_found = False

            for y in range(1, captured_image.height):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if (color_difference > color_difference_threshold):
                    stopping_y.append(y)
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

            y = captured_image.height - 1
            while (y >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if ((color_difference > color_difference_threshold) and (pixel_access_captured_image[x, y][3] != 0)):
                    stopping_y.append(y)
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

                y -= 1

            if ((color_found == False) and (x > captured_image.width * 4 / 10) and (x < captured_image.width * 6 / 10)):
                to_eliminate = True
                break

        for y in range(captured_image.height):
            color_found = False

            for x in range(1, captured_image.width):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if ((color_difference > color_difference_threshold) and (pixel_access_captured_image[x, y][3] != 0)):

                    stopping_x.append(x)
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

            x = captured_image.width - 1
            while (x >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if ((color_difference > color_difference_threshold) and (pixel_access_captured_image[x, y][3] != 0)):

                    stopping_x.append(x)
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)
                x -= 1

            if ((color_found == False) and (y > captured_image.height * 4 / 10) and (y < captured_image.height * 6 / 10)):
                to_eliminate = True
                break

        if (to_eliminate == True):
            return 0

        else:

            x_min = min(stopping_x)
            y_min = min(stopping_y)
            x_max = max(stopping_x)
            y_max = max(stopping_y)

            recaptured_image = captured_image.crop((x_min - 5, y_min - 5, x_max + 5, y_max + 5))
            pixel_access_recaptured_image = recaptured_image.load()

            for x in range(recaptured_image.width):
                for y in range(recaptured_image.height):
                    number_of_blanks_around = 0
                    try:
                        if (pixel_access_recaptured_image[x - 1, y][3] == 0):
                            number_of_blanks_around += 1
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x - 2, y][3] == 0):
                            number_of_blanks_around += 2
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x + 1, y][3] == 0):
                            number_of_blanks_around += 1
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x + 2, y][3] == 0):
                            number_of_blanks_around += 2
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x, y - 1][3] == 0):
                            number_of_blanks_around += 1
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x, y - 2][3] == 0):
                            number_of_blanks_around += 2
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x, y + 1][3] == 0):
                            number_of_blanks_around += 1
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x, y + 2][3] == 0):
                            number_of_blanks_around += 2
                    except:
                        pass

                    if (number_of_blanks_around > 6):
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)

            stopping_x = []
            stopping_y = []
            for x in range(recaptured_image.width):
                for y in range(1, recaptured_image.height):
                    if (pixel_access_recaptured_image[x, y][3] != 0):
                        stopping_y.append(y)
                        break
                    else:
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)

                y = recaptured_image.height - 1
                while (y >= 0):
                    if (pixel_access_recaptured_image[x, y][3] != 0):
                        stopping_y.append(y)
                        break
                    else:
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)
                    y -= 1

            for y in range(recaptured_image.height):
                for x in range(1, recaptured_image.width):
                    if (pixel_access_recaptured_image[x, y][3] != 0):
                        stopping_x.append(x)
                        break
                    else:
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)

                x = recaptured_image.width - 1
                while (x >= 0):
                    if (pixel_access_recaptured_image[x, y][3] != 0):
                        stopping_x.append(x)
                        break
                    else:
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)
                    x -= 1

            x_min = min(stopping_x)
            y_min = min(stopping_y)
            x_max = max(stopping_x)
            y_max = max(stopping_y)

            return recaptured_image.crop((x_min - 5, y_min - 5, x_max + 5, y_max + 5))

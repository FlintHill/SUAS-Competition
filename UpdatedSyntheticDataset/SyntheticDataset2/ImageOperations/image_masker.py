from PIL import Image

class ImageMasker(object):
    """
    Scan all pixels in an image; if any pixel's color is not the intended color1 nor color2, turn that pixel into color1.
    """
    @staticmethod
    def maskImage(image, pixel_data, color1, color2):
        """
        :param image: an image to be masked
        :param pixel_data: the pixel data of the image, obtained by calling image.load()
        :param color1: a criterion of masking, the color to be transformed into
        :param color2: a criterion of masking
        :type image: png, jpg, or other image files
        :type pixel_data: PIL.PyAccess
        :type color1: (R, G, B, A)
        :type color2: (R, G, B, A)
        """
        dimension = image.size

        for x in range(0, dimension[0]):
            for y in range(0, dimension[1]):
                if pixel_data[x, y] != color1 and pixel_data[x, y] != color2:
                   pixel_data[x, y] = color1

        return image

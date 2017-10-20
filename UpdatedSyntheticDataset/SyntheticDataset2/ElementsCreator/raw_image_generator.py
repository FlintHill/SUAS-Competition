from PIL import Image
from PIL import ImageDraw

class RawImageGenerator(object):

    @staticmethod
    def generate_raw_image(width, height, color):
        """
        Generate a mono-colored image
        :param width: the intended width of the image
        :param height: the intended height of the image
        :param color: the intended color of the image
        :type width: int (representing pixels)
        :type height: int (representing pixels)
        :type color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        """
        return Image.new("RGBA", (width, height), color)

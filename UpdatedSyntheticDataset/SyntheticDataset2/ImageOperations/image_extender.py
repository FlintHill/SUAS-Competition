from PIL import Image
from PIL import ImageDraw
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

class ImageExtender(object):

    @staticmethod
    def extend_image(image, extra_width, extra_height):
        """
        Extend the width and/or height of an image in all directions
        :param image: the intended image to modify
        :param extra_width: the intended width to add
        :param extra_height: the inteded height to add
        :type image: an image file
        :type extra_width: an int (representing pixel)
        :type extra_height: an int (representing pixel)
        """
        raw_image = RawImageGenerator.generate_raw_image(image.width+(extra_width*2), image.height+(extra_height*2), (255,255,255,0))
        raw_image.paste(image, (extra_width, extra_height))
        return raw_image

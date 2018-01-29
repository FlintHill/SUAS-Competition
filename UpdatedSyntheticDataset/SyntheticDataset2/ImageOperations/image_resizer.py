from PIL import Image
import math

class ImageResizer(object):

    @staticmethod
    def resize_image_conserved(image, pixelization_level):
        """
        Downscale an image and then upscale the image by the same amount, creating a pixelized effect.
        When inputting a level of pixelization, this specific method outputs the same amount of pixelization
        regardless of the size of the image. In other words, the amount of resizing depends on the size of
        the image, if this is not intended, use the second method in this class.

        :param image: the image to be resized
        :param pixelization_level: the level of pixelization intended (below 20 recommended)
        :type image: an image file
        :type pixelization_level: float
        """
        if pixelization_level <= 0:
            return image

        resize_width_ratio = image.width/1000.0
        resize_height_ratio = image.height/1000.0

        enlarged_image = image.resize((int(image.width/pixelization_level/(resize_width_ratio)), int(image.height/pixelization_level/(resize_height_ratio))))
        resized_image = enlarged_image.resize((int(enlarged_image.width*pixelization_level*(resize_width_ratio)), int(enlarged_image.height*pixelization_level*(resize_height_ratio))))

        return resized_image

    @staticmethod
    def resize_image_free(image, pixelization_level):
        """
        Downscale an image and then upscale the image by the same amount, creating a pixelized effect.
        The amount of pixelization depends on the size of the image input.

        :param image: the image to be resized
        :param pixelization_level: the level of pixelization intended (below 20 recommended)
        :type image: an image file
        :type pixelization_level: float
        """
        if pixelization_level <= 0:
            return image

        enlarged_image = image.resize((int(image.width/pixelization_level), int(image.height/pixelization_level)))
        resized_image = enlarged_image.resize((int(enlarged_image.width*pixelization_level), int(enlarged_image.height*pixelization_level)))

        return resized_image

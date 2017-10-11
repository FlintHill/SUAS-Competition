from PIL import Image

class ImageRotator(object):

    @staticmethod
    def rotate_image(image, angle):
        return image.rotate(angle)

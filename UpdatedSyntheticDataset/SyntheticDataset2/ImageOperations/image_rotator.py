from PIL import Image

class ImageRotator(object):

    @staticmethod
    def find_midpoint(image):
        width = image.width
        height = image.height
        return (width/2, height/2)

    @staticmethod
    def rotate_image(image, angle):
        return image.rotate(angle)

        

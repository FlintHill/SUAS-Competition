from PIL import Image
from SyntheticDataset2.ElementsCreator.raw_image_generator import RawImageGenerator
from .image_paster import ImagePaster
from .bounded_image_cropper import BoundedImageCropper

class ShapeRotator(object):

    @staticmethod
    def rotate_shape(image_input, degree, shape_color):
        background = RawImageGenerator.generate_raw_image(image_input.width*3, image_input.height*3, (255, 255, 255, 0))
        image_with_background = ImagePaster.paste_images(background, image_input)
        rotated_image_with_background = image_with_background.rotate(degree)
        return BoundedImageCropper.crop_bounded_image(rotated_image_with_background, rotated_image_with_background.load(), shape_color)

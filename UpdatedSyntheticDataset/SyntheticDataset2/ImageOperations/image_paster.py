from PIL import Image
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

class ImagePaster(object):

    @staticmethod
    def paste_images(image1, image2):
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), ((image1.height/2)-(image2.height/2))), image2)
        return image1

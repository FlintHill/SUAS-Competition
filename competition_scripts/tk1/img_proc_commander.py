import os
from PIL import Image

CROPS_DIR_LOCATION = "/media/SSD/crops/"
FULL_IMAGES_DIR_LOCATION = "/media/SSD/full_images/"

def load_images_from_dir(dir):
    """
    Load all images in a directory and their associated information files
    """
    images = []

    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file_name in files:
        images.append(Image.open(file_name))

    for file_name in files:
        os.remove(file_name)

    return images

if __name__ == '__main__':
    while True:
        # load Harrison's images
        crops = load_images_from_dir(CROPS_DIR_LOCATION)
        full_images = load_images_from_dir(FULL_IMAGES_DIR_LOCATION)

        # send them to Peter's image processing script

        # transmit the images and their information to the groundstation

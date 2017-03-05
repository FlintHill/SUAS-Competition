
from PIL import Image
def paste_img_onto_img(paste_img, base_img, offset = None):
    base_img.paste(paste_img, box=offset)
    return None

def bw_paste_img_onto_img_same_dim(paste_img, paste_image, base_img, base_image):
    for x in range(0, base_img.size[0]):
        for y in range(0, base_img.size[1]):
            if paste_image[x,y] != 0:
                base_image[x,y] = paste_image[x,y]
    return None
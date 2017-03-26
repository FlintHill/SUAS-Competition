from PIL import Image, ImageOps

def get_bw_rotated_imgs(img, rotation_range, step):
    rotation_imgs = []
    for angle in range(rotation_range[0], rotation_range[1], step):
            if angle != 0:
                append_img = ImageOps.invert(img)
                append_img = append_img.rotate(angle)
                append_img = ImageOps.invert(append_img)
                rotation_imgs.append(append_img)
    return rotation_imgs
from PIL import Image

def scale_img_to_height(img, height, resize_type = Image.NEAREST):
    img_ratio = float(img.size[0])/float(img.size[1])
    return img.resize((int(img_ratio * height), height), resize_type)
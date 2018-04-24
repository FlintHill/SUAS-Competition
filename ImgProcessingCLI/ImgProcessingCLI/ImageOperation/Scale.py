from PIL import Image

def scale_img_to_height(img, height, resize_type = Image.NEAREST):
    img_ratio = float(img.size[0])/float(img.size[1])
    return img.resize((int(img_ratio * height), height), resize_type)

'''scales the image maintaining aspect ratio such that one side is of the dimensions of resize_size'''
def get_img_scaled_to_one_bound(img, resize_size):
    ratio = float(img.size[0])/float(img.size[1])
    if img.size[0] > img.size[1]:
        return img.resize((resize_size, int((1.0/ratio) * resize_size)))
    else:
        return img.resize(((int((ratio) * resize_size)), resize_size))

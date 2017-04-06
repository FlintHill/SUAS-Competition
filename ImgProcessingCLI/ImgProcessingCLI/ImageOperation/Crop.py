from ImgProcessingCLI.Geometry import Rectangle

def get_bw_img_cropped_to_bounds(img, image, margin = 0):
    bounds = get_bw_img_bounds(img, image)
    bounds.set_x(bounds.get_x() - margin)
    bounds.set_y(bounds.get_y() - margin)
    bounds.set_width(bounds.get_width() + 1 + margin * 2)
    bounds.set_height(bounds.get_height() + 1 + margin * 2)
    img_out = get_img_cropped_to_bounds(img, bounds)
    image = img_out.load()
    return img_out

def get_bw_img_bounds(img, image):
    left_x = img.size[0]
    right_x = 0
    up_y = img.size[1]
    down_y = 0
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            if image[x,y] != 0:
                if x < left_x:
                    left_x = x
                if x > right_x:
                    right_x = x
                if y < up_y:
                    up_y = y
                if y > down_y:
                    down_y = y
    return Rectangle(left_x, up_y, (right_x - left_x), (down_y - up_y))

def get_img_cropped_to_bounds(img, rect):
    return img.crop((rect.get_x(), rect.get_y(), rect.get_x() + rect.get_width(), rect.get_y() + rect.get_height()))

from Geometry.Rectangle import Rectangle

def get_bw_img_cropped_to_bounds(img, image):
    return get_img_cropped_to_bounds(img, get_bw_img_bounds(img, image))

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
    
    
from PIL import Image

def get_bmp_masked_img(mask_img, mask_image, base_img, base_image, offset = (0,0)):
    out_img = Image.new("RGBA", base_img.size, (0,0,0,0))
    out_image = out_img.load()
    for x in range(offset[0], mask_img.size[0] + offset[0]):
        for y in range(offset[1], mask_img.size[1] + offset[1]):
            if mask_image[x-offset[0], y-offset[0]] != 0:
                out_image[x,y] = base_image[x,y]
    return out_img
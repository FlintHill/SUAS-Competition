'''takes a black and white image and returns the image after the kernel is convoluted over it'''
def convolute(img_in, kernel):
    image_original = img_in.load()
    img = img_in.copy()
    image = img.load()
    for x in range(int((len(kernel) - 1)/2), img.size[0] - int((len(kernel)-1)/2)):
        for y in range(int((len(kernel[0])-1)/2), img.size[1] - int((len(kernel[0])-1)/2)):
            image[x,y] = int(get_kernel_sum_of_pixel((x,y), image_original, kernel))
    return img

def convolute_array(img_in, kernel):
    image_original = img_in.load()
    arr = [[0 for j in range(0, img_in.size[1])] for i in range(0, img_in.size[0])]
    for x in range(int((len(kernel) - 1)/2), len(arr) - int((len(kernel)-1)/2)):
        for y in range(int((len(kernel[0])-1)/2), len(arr[0]) - int((len(kernel[0])-1)/2)):
            arr[x][y] = int(get_kernel_sum_of_pixel((x,y), image_original, kernel))
    return arr

def get_kernel_sum_of_pixel(pixel, image, kernel):
    sum = 0
    gap_num = int((len(kernel)-1)/2)
    for i in range(0, len(kernel)):
        for j in range(0, len(kernel[0])):
            sum += kernel[i][j] * image[pixel[0] + gap_num - i, pixel[1] + gap_num - j]
    return sum

def crop_img_to_kernel_bounds(img, image, kernel_size):
    out_img = img.crop((int((kernel_size-1)/2), int((kernel_size-1)/2), img.size[0] - int((kernel_size-1)/2), img.size[1] - int((kernel_size-1)/2)))
    return out_img

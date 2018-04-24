import ImgProcessingCLI.KernelOperations
import ImgProcessingCLI.KernelOperations.KernelMath as KernelMath
import ImgProcessingCLI.ImageOperation
import ImgProcessingCLI.ImageOperation.ImageMath as ImageMath

def get_mean_blurred_bw_img(img, image, kernel_size):
    kernel = get_kernel(kernel_size)
    return KernelMath.convolute(img, kernel)

def get_mean_blurred_rgb_img(img, image, kernel_size):
    split_img = img.split()
    r_img = get_mean_blurred_bw_img(split_img[0].convert('L'), split_img[0].convert('L').load(), kernel_size)
    g_img = get_mean_blurred_bw_img(split_img[1].convert('L'), split_img[1].convert('L').load(), kernel_size)
    b_img = get_mean_blurred_bw_img(split_img[2].convert('L'), split_img[2].convert('L').load(), kernel_size)
    return ImageMath.merge_channels(img.size, [r_img.load(), g_img.load(), b_img.load()])

def get_kernel(kernel_size):
    return [[1.0/float(kernel_size**2) for i in range(0, kernel_size)] for j in range(0, kernel_size)]

from PIL import Image
from math import sqrt, exp
import ImgProcessingCLI.NoiseReduction.GaussianBlur as GaussianBlur
import ImgProcessingCLI.KernelOperations.KernelMath as KernelMath

KERNEL_SIZE = 3

def get_gray_img_to_scale_space(img, image, num_iter, t_max):
    imgs = [img]
    t_key = []
    t_step = float(t_max-1)/float(num_iter)
    t = 1 + t_step
    for i in range(1, num_iter + 1):
        sigma_target = sqrt(t)
        sigma_before = sqrt(t-t_step)
        sigma_step = sqrt(sigma_target**2 - sigma_before**2)
        print("sigma step: ", sigma_step)
        append_img = GaussianBlur.get_gaussian_filtered_bw_img(imgs[len(imgs)-1], imgs[len(imgs)-1].load(), KERNEL_SIZE, sigma_step)
        #append_img.show()

        imgs.append(append_img.resize((int(img.size[0]/t), int(img.size[1]/t))))
        t += t_step
        t_key.append(t)

    del imgs[0]

    print("t key: ", t_key)
    return tuple(imgs), tuple(t_key)

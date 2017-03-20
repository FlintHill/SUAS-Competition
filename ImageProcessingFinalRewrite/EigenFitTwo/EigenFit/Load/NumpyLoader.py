import numpy
import os
from PIL import Image, ImageOps
import EigenFit.Vector.VectorMath as VectorMath
import EigenFit.Load.FileFunctions as FileFunctions
def load_numpy_arr(path):
    return numpy.load(path)

def load_imgs_as_gray_numpy(path, extension, resize = False, invert = False):
    file_names = os.listdir(path)
    FileFunctions.remove_names_without_extension(file_names, extension)
    imgs = []
    for i in range(0, len(file_names)):
        imgs.append(Image.open(path + "/" + file_names[i]).convert('L'))
        if resize != False:
            imgs[i] = imgs[i].resize(resize)
        if invert == True:
            imgs[i] = ImageOps.invert(imgs[i])
    img_vectors = []
    for i in range(0, len(imgs)):
        img_vectors.append(VectorMath.gray_img_to_vector(imgs[i]))
    return numpy.asarray(img_vectors)
    

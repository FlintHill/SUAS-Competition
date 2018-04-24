import numpy
from PIL import Image

def gray_img_to_vector(img):
    img_vector = numpy.array(img)
    img_vector = img_vector.flatten()
    return img_vector

def img_vector_to_gray_img(vector, dim):
    img = Image.new('L', dim, 0)
    image = img.load()
    for i in range(0, vector.shape[0]):
        image[i%(dim[0]), int(i/dim[0])] = int(vector[i])
    return img
    
def gray_imgs_to_vectors(imgs):
    vectors = []
    for i in range(0, len(imgs)):
        vectors.append(gray_img_to_vector(imgs[i]))
    return numpy.asarray(vectors) 

def unit_vector(vector):
    return vector * 1.0/numpy.linalg.norm(vector)
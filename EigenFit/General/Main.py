from PIL import Image, ImageOps
from EigenFit import *
import numpy
import random
from ImgProcessingCLI.ImageOperation import *
import ImgProcessingCLI.ImageOperation.Crop as Crop
import string

base_path = "/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/New EigenFaces"
img_dimensions = (300,400)
'''
imgs = FileFunctions.load_imgs(FileFunctions.get_paths_with_extension(base_path + "/Training", ".jpg"))
for i in range(0, len(imgs)):
    imgs[i] = imgs[i].resize(img_dimensions)
    imgs[i] = imgs[i].convert('L')
img_vectors = VectorMath.gray_imgs_to_vectors(imgs)
eigen_maker = EigenMaker(img_vectors)
NumpySaver.save_array(eigen_maker.get_eigenvectors(), base_path + "/Data/Eigenvectors", "eigenvectors.npy")
NumpySaver.save_array(eigen_maker.get_mean_img_vector(), base_path + "/Data/Mean", "mean_img.npy")
'''

'''

eigenvectors = numpy.asarray(NumpyLoader.load_numpy_arr(base_path + "/Data/Eigenvectors/eigenvectors.npy"))
mean_img = NumpyLoader.load_numpy_arr(base_path+"/Data/Mean/mean_img.npy")


letter_path = base_path + "/Training"
face_imgs = FileFunctions.load_imgs(FileFunctions.get_paths_with_extension(letter_path, ".jpg"))


for i in range(0, len(face_imgs)):
    face_imgs[i] = face_imgs[i].resize(img_dimensions)

letter_projection_saver = ProjectionSaver(face_imgs, eigenvectors, mean_img, base_path + "/Data/Projections/" + "Faces")


num_dims = 75
projections = NumpyLoader.load_numpy_arr(base_path + "/Data/Projections/Faces/projection.npy")[:, 0:num_dims]
print("projections size: " + str(projections.shape))
mean_img = NumpyLoader.load_numpy_arr(base_path +"/Data/Mean/mean_img.npy")
eigenvectors = numpy.asarray(NumpyLoader.load_numpy_arr(base_path + "/Data/Eigenvectors/eigenvectors.npy"))[0:num_dims, :]

print("eigenvectors size: " + str(eigenvectors.shape))
img_save_path = base_path + "/Generated Faces"
for j in range(0, 30):
    std_dev_vector = numpy.std(projections, axis = 0)
    rand_projection = numpy.zeros((std_dev_vector.shape[0]))

    for i in range(0, rand_projection.shape[0]):
        rand_projection[i] = random.gauss(0, std_dev_vector[i])





    reconstruction_vector = EigenProjector.get_reconstruction_img_vector(rand_projection, eigenvectors)+mean_img
    VectorMath.img_vector_to_gray_img(reconstruction_vector, img_dimensions).save(img_save_path + "/Face " + str(j), "PNG")

'''


def get_imgs_resized_to_PCA_specs(imgs, img_dim):
    out_imgs = []

    for i in range(0, len(imgs)):
        out_imgs.append(resize_img_to_PCA_specs(imgs[i], img_dim))
    return out_imgs


def resize_img_to_PCA_specs(img, img_dim):
    crop_img = img
    crop_img = Crop.get_bw_img_cropped_to_bounds(ImageOps.invert(img.convert('L')), ImageOps.invert(img.convert('L')).load())
    crop_img = crop_img.resize(img_dim)
    return crop_img


base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/180 ORIENTATION PCA"
#projections = NumpyLoader.load_numpy_arr(base_path + "/Data/Projections/" + letter + "/projection.npy")[:, 0:num_dims]
#rotation_range = (-5, 5)
#rotation_step = 2
img_dimensions = (40,40)


imgs = FileFunctions.load_imgs(FileFunctions.get_paths_with_extension( base_path + "/Training", ".png"))

imgs = get_imgs_resized_to_PCA_specs(imgs, img_dimensions)
non_rotated_imgs = list(imgs)
append_imgs = []
for i in range(0, len(imgs)):
    for j in range(0, 8):
        append_imgs.append(resize_img_to_PCA_specs(ImageOps.invert(imgs[i].rotate(j*45, expand=True)), img_dimensions))

append_imgs[0].show()
#imgs.extend(append_imgs)
imgs = list(append_imgs)
img_vectors = VectorMath.gray_imgs_to_vectors(imgs)#NumpyLoader.load_imgs_as_gray_numpy(base_path + "/Training", ".png", resize = (40,40), invert = False)
eigen_maker = EigenMaker(img_vectors)
NumpySaver.save_array(eigen_maker.get_eigenvectors(), base_path + "/Data/Eigenvectors", "eigenvectors 0.npy")
NumpySaver.save_array(eigen_maker.get_mean_img_vector(), base_path + "/Data/Mean", "mean_img 0.npy")


eigenvectors = NumpyLoader.load_numpy_arr(base_path + "/Data/Eigenvectors/" + "eigenvectors 0.npy")
mean_img = NumpyLoader.load_numpy_arr(base_path + "/Data/Mean" + "/mean_img 0.npy")


letters = string.ascii_uppercase#map(chr, range(65, 91))


right_side_projections = []


#for i in range(0, len(non_rotated_imgs)):
for rotation_index in range(0, 8):
    projection_imgs = list(non_rotated_imgs)
    for j in range(0, len(projection_imgs)):
        projection_imgs[j] = resize_img_to_PCA_specs(ImageOps.invert((projection_imgs[j]).rotate(rotation_index * 45, expand = True)), img_dimensions)

    projection_imgs[0].show()
    projections = []
    for j in range(0, len(projection_imgs)):
        img_vector = VectorMath.gray_img_to_vector(projection_imgs[j])
        projection_weights = EigenProjector.get_projection_weights(img_vector, eigenvectors, mean_img)
        projections.append(projection_weights)


    NumpySaver.save_array(numpy.asarray(projections), base_path + "/Data/Projections/" + str(rotation_index), "projection.npy")


'''
for i in range(0, len(letters)):
    letter = str(letters[i])

    letter_path = "/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/SUASLetterImgs/Imgs/" + letter + "/Training"

    letter_imgs = FileFunctions.load_imgs(FileFunctions.get_paths_with_extension(letter_path, ".png"))
    letter_imgs = get_imgs_resized_to_PCA_specs(letter_imgs, img_dimensions)

    #projections = []
    for j in range(0,len(letter_imgs)):
        img = letter_imgs[j]#Image.open("/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/SUASLetterImgs/Imgs/A/Training/img011-00001.png").convert('L').resize((40,40))
        img_vector = VectorMath.gray_img_to_vector(img)
        print("img vector: " + str(img_vector))
        projection_weights = EigenProjector.get_projection_weights(img_vector, eigenvectors, mean_img)
        right_side_projections.append(projection_weights)
    #NumpySaver.save_array(numpy.asarray(projections), base_path + "/Data/Projections/" + letters[i], "projection.npy")


    img = letter_imgs[0]#Image.open("/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/SUASLetterImgs/Imgs/A/Training/img011-00001.png").convert('L').resize((40,40))
    img_vector = VectorMath.gray_img_to_vector(img)
    print("img vector: " + str(img_vector))
    projection_weights = EigenProjector.get_projection_weights(img_vector, eigenvectors, mean_img)[0:20]
    reconstruction_vector = EigenProjector.get_reconstruction_img_vector(projection_weights, eigenvectors) + mean_img
    print("reconstruction_vector: " + str(reconstruction_vector))
    #VectorMath.img_vector_to_gray_img(img_vector, img_dimensions).show()
    VectorMath.img_vector_to_gray_img(reconstruction_vector, img_dimensions).show()
NumpySaver.save_array(numpy.asarray(right_side_projections), base_path + "/Data/Projections/Correct", "projection.npy")
'''

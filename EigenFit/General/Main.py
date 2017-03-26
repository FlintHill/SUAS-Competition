from PIL import Image, ImageOps
from EigenFit import *
import numpy
import random

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







base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/NEWLETTERPCA WITH ROTATIONS"
#projections = NumpyLoader.load_numpy_arr(base_path + "/Data/Projections/" + letter + "/projection.npy")[:, 0:num_dims]
#rotation_range = (-5, 5)
#rotation_step = 2
img_dimensions = (40,40)

imgs = FileFunctions.load_imgs(FileFunctions.get_paths_with_extension( base_path + "/Training", ".png"))
rotated_imgs = []
for i in range(0, len(imgs)):
    imgs[i] = imgs[i].resize(img_dimensions)
    rotated_imgs.append(imgs[i].rotate(180))
    #append_rotated_imgs = ImageOperations.get_bw_rotated_imgs(imgs[i], rotation_range, rotation_step)
    #for j in range(0, len(append_rotated_imgs)):
        #rotated_imgs.append(append_rotated_imgs[j])

for i in range(0, len(rotated_imgs)):
    imgs.append(rotated_imgs[i])

img_vectors = VectorMath.gray_imgs_to_vectors(imgs)#NumpyLoader.load_imgs_as_gray_numpy(base_path + "/Training", ".png", resize = (40,40), invert = False)
eigen_maker = EigenMaker(img_vectors)
NumpySaver.save_array(eigen_maker.get_eigenvectors(), base_path + "/Data/Eigenvectors", "eigenvectors 0.npy")
NumpySaver.save_array(eigen_maker.get_mean_img_vector(), base_path + "/Data/Mean", "mean_img 0.npy")


eigenvectors = NumpyLoader.load_numpy_arr(base_path + "/Data/Eigenvectors/" + "eigenvectors 0.npy")
mean_img = NumpyLoader.load_numpy_arr(base_path + "/Data/Mean" + "/mean_img 0.npy")
letters = map(chr, range(65, 91))
for i in range(0, len(letters)):
    letter = str(letters[i])

    letter_path = "/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/SUASLetterImgs/Imgs/" + letter + "/Training"
    letter_imgs = FileFunctions.load_imgs(FileFunctions.get_paths_with_extension(letter_path, ".png"))
    for j in range(0, len(letter_imgs)):
        letter_imgs[j] = letter_imgs[j].resize(img_dimensions)
        letter_imgs[j] = letter_imgs[j].rotate(180, expand = True)

    '''
    for i in range(0, len(letter_imgs)):
        letter_imgs[i] = letter_imgs[i].resize(img_dimensions)

    append_letters = ImageOperations.get_bw_rotated_imgs(letter_imgs[i], rotation_range, rotation_step)

    for i in range(0, len(append_letters)):
        letter_imgs.append(append_letters[i])
    '''
    letter_projection_saver = ProjectionSaver(letter_imgs, eigenvectors, mean_img, base_path + "/Data/Projections180/" + letter + "180")



    img = letter_imgs[0]#Image.open("/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/SUASLetterImgs/Imgs/A/Training/img011-00001.png").convert('L').resize((40,40))
    img_vector = VectorMath.gray_img_to_vector(img)
    projection_weights = EigenProjector.get_projection_weights(img_vector, eigenvectors, mean_img)
    reconstruction_vector = EigenProjector.get_reconstruction_img_vector(projection_weights, eigenvectors) + mean_img
    VectorMath.img_vector_to_gray_img(reconstruction_vector, (40,40)).show()

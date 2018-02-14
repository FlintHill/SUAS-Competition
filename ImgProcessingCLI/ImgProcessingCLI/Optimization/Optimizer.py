import EigenFit.Load.NumpyLoader as NumpyLoader
import EigenFit.Vector.VectorMath as VectorMath
import EigenFit.Vector.EigenProjector as EigenProjector
import EigenFit.Load.FileFunctions as FileFunctions
import os
import string
from PIL import Image
import numpy

class Optimizer:
    def __init__(self, classifier, training_path, testing_path, num_dim, img_extension):
        #self.eigenvectors = eigenvectors
        #self.mean_img_vector = mean_img_vector
        self.img_extension = img_extension
        self.training_path = training_path
        self.testing_path = testing_path
        self.num_dim = num_dim
        self.classifier = classifier
        self.train()
        self.get_test_score()

    def train(self):
        self.eigenvectors = NumpyLoader.load_numpy_arr(self.training_path + "/Data/Eigenvectors/eigenvectors 0.npy")
        self.mean_img_vector = NumpyLoader.load_numpy_arr(self.training_path + "/Data/Mean/mean_img 0.npy")
        self.test_data = []
        self.test_targets = []
        test_data_names = os.listdir(self.training_path + "/Data/Projections")
        FileFunctions.remove_dirs_that_arent_folders(test_data_names)
        letters = string.ascii_uppercase
        for i in range(0, len(test_data_names)):
            letter_projections = NumpyLoader.load_numpy_arr(self.training_path + "/Data/Projections/" + str(letters[i]) + "/projection.npy")
            for projection_index in range(0, letter_projections.shape[0]):
                self.test_data.append(letter_projections[projection_index][0:self.num_dim])
                self.test_targets.append(i)
        self.classifier.fit(self.test_data, self.test_targets)

    def get_test_score(self):
        test_imgs = []
        img_names = os.listdir(self.testing_path + "/Images")
        FileFunctions.remove_names_without_extension(img_names, self.img_extension)
        img_names = sorted(img_names, key = lambda name : int(name[0:name.index(".")]))
        for i in range(0, len(img_names)):
            test_imgs.append(Image.open(self.testing_path + "/Images/"  + img_names[i]).convert('L'))
        answer_key = list(NumpyLoader.load_numpy_arr(self.testing_path + "/Answers/answers.npy"))
        test_projections = self.get_projection_weights_of_imgs(test_imgs)
        predictions = numpy.asarray(self.classifier.predict(test_projections))
        letters = string.ascii_uppercase
        answer_key_nums = numpy.asarray([letters.index(answer_key[i]) for i in range(0, len(answer_key))])

        correct_arr = numpy.subtract(predictions, answer_key_nums)
        num_correct = 0
        for i in range(0, correct_arr.shape[0]):
            if correct_arr[i] == 0:
                num_correct += 1
        return num_correct


    def predict_letter(self, img):
        letters = string.ascii_uppercase
        projection_weights = self.get_projection_weights_of_img(img)
        return letters[self.classifier.predict(projection_weights)[0]]

    def get_projection_weights_of_imgs(self, imgs):
        projections = []
        for i in range(0, len(imgs)):
            projections.append(self.get_projection_weights_of_img(imgs[i]))
        return projections

    def get_projection_weights_of_img(self, img):
        img_projection = VectorMath.gray_img_to_vector(img)
        projection_weights = EigenProjector.get_projection_weights(img_projection, self.eigenvectors, self.mean_img_vector)[0:self.num_dim]
        return projection_weights

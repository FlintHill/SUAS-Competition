import numpy
import scipy

import EigenFit.Vector.VectorMath as VectorMath

class EigenMaker(object):

    def __init__(self, img_vectors):
        self.img_vectors = img_vectors
        print(self.img_vectors)

        self.mean_img_vector = numpy.mean(self.img_vectors, 0)
        VectorMath.img_vector_to_gray_img(self.mean_img_vector, (40,40)).show()
        print("mean: " + str(self.mean_img_vector))

        self.mean_adjusted_imgs = self.img_vectors - self.mean_img_vector

        print("mean adjusted imgs: " + str(self.mean_adjusted_imgs))

        self.eigenvectors, self.eigenvalues, self.right_vectors = numpy.linalg.svd(self.mean_adjusted_imgs.transpose(), full_matrices = False)
        self.eigenvectors = self.eigenvectors.transpose()
        self.right_vectors = self.right_vectors.transpose()

    def get_eigenvectors(self):
        return self.eigenvectors

    def get_mean_img_vector(self):
        return self.mean_img_vector

from EigenFit.Vector import *
from EigenFit.Save import *
import numpy

class ProjectionSaver(object):

    def __init__(self, imgs, eigenvectors, mean, path):
        self.path = path
        self.imgs = imgs
        self.eigenvectors = eigenvectors
        self.mean = mean
        self.save_projections()

    def save_projections(self):
        projections = []
        for i in range(0, len(self.imgs)):
            img_vector = VectorMath.gray_img_to_vector(self.imgs[i])
            projection_weights = EigenProjector.get_projection_weights(img_vector, self.eigenvectors, self.mean)
            projections.append(projection_weights)
            #NumpySaver.save_array(projection_weights, self.path, "projection " + str(i) + ".npy")
        NumpySaver.save_array(numpy.asarray(projections), self.path, "projection.npy")

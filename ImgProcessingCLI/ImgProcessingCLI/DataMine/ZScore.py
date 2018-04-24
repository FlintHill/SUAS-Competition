import numpy
import ImgProcessingCLI.ImgVector.VectorMath as VectorMath

class ZScore(object):
    def __init__(self, name_in, projections_in):
        self.name = name_in
        self.projections = projections_in
        self.init_stats()

    def init_stats(self):
        self.mean_projection = numpy.average(self.projections, axis = 0)
        self.std_dev_vector = numpy.std(self.projections, axis = 0)
        self.std_dev_mag = numpy.linalg.norm(self.std_dev_vector)
        #print(self.name + ": " + str(self.std_dev))

    def get_fit_score(self, img_projection, thresholds = None):
        dist = VectorMath.mag_between_vectors(img_projection, self.mean_projection)
        return dist/self.std_dev_mag

    def __repr__(self):
        return self.name

import ImgProcessingCLI.ImgVector.VectorMath as VectorMath

class KNearestNeighbors(object):
    def __init__(self, name_in, projections_in):
        self.name = name_in
        self.projections = projections_in

    '''thresholds for KNN is the radius of the sphere it looks within to count projections'''
    def get_fit_score(self, img_projection, radius_threshold):
        num_in_radius = 0
        for i in range(0, len(self.projections)):
            mag_between_vectors = VectorMath.mag_between_vectors(img_projection, self.projections[i])
            if mag_between_vectors < radius_threshold:
                num_in_radius += 1
        return num_in_radius

    def __repr__(self):
        return self.name

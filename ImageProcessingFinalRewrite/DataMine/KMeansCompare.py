from ImgStat.KMeans import KMeans
import numpy
import ImgVector.VectorMath as VectorMath

class KMeansCompare:
    CLUSTERS_PER_LETTER = 8
    TIMES_TO_RUN = 30
    def __init__(self, name_in, projections_in):
        self.name = name_in
        self.projections = projections_in
        self.init_kmeans()
        
    def init_kmeans(self):
        self.kmeans = KMeans.init_with_numpy(self.projections, KMeansCompare.CLUSTERS_PER_LETTER, KMeansCompare.TIMES_TO_RUN)
    
    def get_fit_score(self, img_projection, thresholds = None):
        closest_cluster = self.kmeans.get_clusters().get_closest_cluster_to_vector(img_projection)
        dist_between = VectorMath.mag_between_vectors(numpy.asarray(closest_cluster.get_origin()), numpy.asarray(img_projection))
        return dist_between

    def __repr__(self):
        return self.name

'''from ImgStat.KMeans import KMeans
from Stat.EigenImageProjector import EigenImageProjector
import Vector.VectorMath as VectorMath
import numpy

class KMeansCompare:
    CLUSTERS_PER_LETTER = 3
    TIMES_TO_RUN = 30
    
    def __init__(self, name_in, compare_data_loader_in, projections_in):
        self.projections = projections_in
        
        self.name = name_in
        self.compare_data_loader = compare_data_loader_in
        self.init_kmeans()
        
    
    def init_kmeans(self):
        self.kmeans = KMeans.init_with_numpy(self.projections, KMeansCompare.CLUSTERS_PER_LETTER, KMeansCompare.TIMES_TO_RUN)
    
    def get_fit_score(self, img_projection, thresholds = None):
        closest_cluster = self.kmeans.get_clusters().get_closest_cluster_to_vector(img_projection)
        dist_between = VectorMath.mag_between_vectors(numpy.asarray(closest_cluster.get_origin()), numpy.asarray(img_projection))
        return dist_between

    def __repr__(self):
        return self.name
        
'''
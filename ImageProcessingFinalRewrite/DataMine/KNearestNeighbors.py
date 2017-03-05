import numpy
class KNearestNeighbors:
    
    '''compare_point and compare_data must both be numpy arrays'''
    def __init__(self, name_in, compare_data_loader_in):
        #self.compare_point = compare_point_in
        self.name = name_in
        self.compare_data_loader = compare_data_loader_in
        #self.knn_radius = args_in[0]
        #self.init_num_neighbors()
    
    def get_fit_score(self, compare_img, knn_radius):
        img_projector = EigenImageProjector(self.compare_data_loader, compare_img)
        img_projection = img_projector.get_img_projection()
        #img_projection = numpy.subtract(img_projection, self.compare_data_loader.get_mean)
        num_neighbors = 0
        for i in range(0, self.compare_data_loader.get_projections().shape[0]):
            distance_between = VectorMath.mag_between_vectors(img_projection, self.compare_data_loader.get_projections()[i])
            if distance_between < knn_radius:
                num_neighbors += 1
    
        return num_neighbors
    
    def __repr__(self):
        return self.name
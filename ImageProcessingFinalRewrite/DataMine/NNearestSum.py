import numpy
import NoiseReduction.GaussianBlur as GaussianBlur
class NNearestSum:
    def __init__(self, name_in, compare_data_loader_in, projections_in):
        self.projections = projections_in
        print("algo projections; " + str(self.projections))
        self.name = name_in
        self.compare_data_loader = compare_data_loader_in
        
    def get_fit_score(self, img_projection, num_points):
        #compare_img = GaussianBlur.get_gaussian_filtered_bw_img(compare_img, compare_img.load(), 3, 2)
        #img_projector = EigenImageProjector(self.compare_data_loader, compare_img)
        #img_projection = img_projector.get_img_projection()
        sorted_compare_projections = self.get_projections_sorted_by_distance(img_projection)
        sum = 0
        for i in range(0, num_points):
            sum += numpy.linalg.norm( numpy.subtract(img_projection, sorted_compare_projections[i]) )
        #std_dev = self.compare_data_loader.get_std_dev_of_projections()
        '''if std_dev == 0:
            return 0
        return sum/float(std_dev)'''
        return sum#/float(std_dev)
        
    def get_projections_sorted_by_distance(self, projection):
        return sorted(self.projections, key = lambda compare_projection: VectorMath.mag_between_vectors(compare_projection, projection))
    
    def __repr__(self):
        return self.name
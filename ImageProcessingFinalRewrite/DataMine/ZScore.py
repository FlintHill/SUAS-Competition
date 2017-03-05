
import numpy

class ZScore:
    def __init__(self, name_in, compare_data_loader_in):
        self.name = name_in
        self.compare_data_loader = compare_data_loader_in
        
    def get_fit_score(self, compare_img, thresholds = None):
        img_projector = EigenImageProjector(self.compare_data_loader, compare_img)
        img_projection = img_projector.get_img_projection()
        projection_minus_mean = numpy.subtract(img_projection, self.compare_data_loader.get_mean_projection())
        return numpy.linalg.norm(projection_minus_mean)/self.compare_data_loader.get_std_dev_of_projections()
    
    def __repr__(self):
        return self.name
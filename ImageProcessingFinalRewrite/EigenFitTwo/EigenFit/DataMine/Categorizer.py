import os
import EigenFit.Load.FileFunctions as FileFunctions
from EigenFit.DataMine.NamedProjections import NamedProjections
import EigenFit.Load.NumpyLoader as NumpyLoader
import EigenFit.Vector.EigenProjector as EigenProjector
import EigenFit.Vector.VectorMath as VectorMath
import numpy
class Categorizer:
    
    def __init__(self, eigenvectors, mean, projections_path, compare_algorithm, num_dims):
        self.num_dims = num_dims
        self.mean = mean
        self.compare_algorithm = compare_algorithm
        self.projections_path = projections_path
        self.eigenvectors = eigenvectors[0:num_dims]
        self.init_projection_dirs()
        self.init_named_projections()
        self.init_algorithm_instances()
        
    def init_projection_dirs(self):
        names = os.listdir(self.projections_path)
        self.directories = [self.projections_path + "/" + names[i] for i in range(0, len(names))]
        FileFunctions.remove_dirs_that_arent_folders(self.directories)
        
    def init_named_projections(self):
        self.named_projections = []
        for i in range(0, len(self.directories)):
            self.named_projections.append(NamedProjections(os.path.basename(os.path.normpath(self.directories[i])), numpy.asarray(NumpyLoader.load_numpy_arr(FileFunctions.get_max_filepath(self.directories[i])))[:,0:self.num_dims]))
           
    
    def get_algorithm_return_smallest_to_large(self, compare_img, thresholds):
        img_projection = VectorMath.gray_img_to_vector(compare_img)
        projection_weights = EigenProjector.get_projection_weights(img_projection, self.eigenvectors, self.mean)
        output = sorted(self.algorithm_instances, key = lambda algo_instance: algo_instance.get_fit_score(projection_weights))
        for i in range(0, len(output)):
            score = output[i].get_fit_score(projection_weights, thresholds)
            output[i] = (output[i], score)
        return output
 
    def init_algorithm_instances(self):
        self.algorithm_instances = []
        for i in range(0, len(self.named_projections)):
            append_algo = self.compare_algorithm(self.named_projections[i].get_name(), self.named_projections[i].get_projections())
            self.algorithm_instances.append(append_algo)
            
    def get_named_projections(self):
        return self.named_projections
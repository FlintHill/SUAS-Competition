from ImgProcessingCLI.General.TargetTwo import TargetTwo
import EigenFit.Load.NumpyLoader as NumpyLoader
from EigenFit.DataMine.Categorizer import Categorizer
from ImgProcessingCLI.DataMine.OrientationSolver import OrientationSolver
from ImgProcessingCLI.DataMine.KMeansCompare import KMeansCompare

class TargetFunneler(object):

    def __init__(self, letter_pca_path, letter_categorizer_dims, orientation_pca_path, orientation_dims):
        self.init_letter_categorizer(letter_pca_path, letter_categorizer_dims)
        self.init_orientation_solver(orientation_pca_path, orientation_dims)

    def init_letter_categorizer(self, letter_pca_path, letter_categorizer_dims):
        eigenvectors = NumpyLoader.load_numpy_arr(letter_pca_path + "/Data/Eigenvectors/eigenvectors 0.npy")
        projections_path = letter_pca_path + "/Data/Projections"
        mean = NumpyLoader.load_numpy_arr(letter_pca_path + "/Data/Mean/mean_img 0.npy")
        self.letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, letter_categorizer_dims)

    def init_orientation_solver(self, orientation_pca_path, orientation_dims):
        orientation_eigenvectors = NumpyLoader.load_numpy_arr(orientation_pca_path + "/Data/Eigenvectors/eigenvectors 0.npy")
        orientation_projections_path = orientation_pca_path + "/Data/Projections"
        orientation_mean = NumpyLoader.load_numpy_arr(orientation_pca_path + "/Data/Mean/mean_img 0.npy")
        self.orientation_solver = OrientationSolver(orientation_eigenvectors, orientation_mean, orientation_pca_path, orientation_dims)

    def init_target(self, target_img):
        return TargetTwo(target_img, target_img.load(), self.letter_categorizer, self.orientation_solver)

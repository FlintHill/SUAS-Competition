import ImgProcessingCLI.TargetTrait.FalseCropCatcher as FalseCropCatcher
from ImgProcessingCLI.Runtime.RuntimeTarget import RuntimeTarget
import EigenFit.Load.NumpyLoader as NumpyLoader
from EigenFit.DataMine.Categorizer import Categorizer
import EigenFit.Load.FileFunctions as FileFunctions
from ImgProcessingCLI.DataMine.KMeansCompare import KMeansCompare
from ImgProcessingCLI.DataMine.OrientationSolver import OrientationSolver
import ImgProcessingCLI.Runtime.TimeOps as TimeOps
import os
from PIL import Image

class CompetitionInput(object):

    def __init__(self, full_img_path, crop_img_extension, letter_categorizer_path, letter_categorizer_num_dim, orientation_solver_path, orientation_solver_num_dim, geo_stamps):
        self.init_crop_imgs(full_img_path, crop_img_extension)
        self.geo_stamps = geo_stamps
        self.remove_false_positives()

        self.init_categorizers(letter_categorizer_path, letter_categorizer_num_dim, orientation_solver_path, orientation_solver_num_dim)
        self.init_targets()



    '''initializes the list of crop images using the image path'''
    def init_crop_imgs(self, crop_img_path, crop_img_extension):
        img_names = os.listdir(crop_img_path)
        FileFunctions.remove_names_without_extension(img_names, crop_img_extension)
        img_paths = [crop_img_path + "/" + img_names[i] for i in range(0, len(img_names))]

        self.crop_imgs = [Image.open(img_paths[i]) for i in range(0, len(img_paths))]
        #self.time_first_img_taken = TimeOps.str_time_to_seconds(self.crop_imgs[0]._getexif()[36867])
        earliest_time = TimeOps.str_time_to_seconds(self.crop_imgs[0]._getexif()[36867])
        for i in range(1, len(self.crop_imgs)):
            iter_time = TimeOps.str_time_to_seconds(self.crop_imgs[i]._getexif()[36867])
            if iter_time < earliest_time:
                earliest_time = iter_time
        self.time_first_img_taken = earliest_time
        '''list of original image times created'''
        self.crop_img_times = []
        for i in range(0, len(self.crop_imgs)):
            self.crop_img_times.append(TimeOps.str_time_to_seconds(self.crop_imgs[i]._getexif()[36867]))

        '''crop the images to targets, and make sure that the crop times are perfectly aligned with
        crop list.'''
        return None




    '''kills the false positives in the set using the FalseCropCatcher'''
    def remove_false_positives(self):
        i = 0
        while i < len(self.crop_imgs):
            is_false_positive = FalseCropCatcher.get_if_is_false_positive(self.crop_imgs[i], self.crop_imgs[i].load())
            if is_false_positive:
                del self.crop_imgs[i]
            else:
                i += 1

    def init_categorizers(self, letter_categorizer_path, letter_categorizer_num_dim, orientation_solver_path, orientation_solver_num_dim):
        eigenvectors = NumpyLoader.load_numpy_arr(letter_categorizer_path + "/Data/Eigenvectors/eigenvectors 0.npy")
        projections_path = letter_categorizer_path + "/Data/Projections"
        mean = NumpyLoader.load_numpy_arr(letter_categorizer_path + "/Data/Mean/mean_img 0.npy")

        self.letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, letter_categorizer_num_dim)

        orientation_eigenvectors = NumpyLoader.load_numpy_arr(orientation_solver_path + "/Data/Eigenvectors/eigenvectors 0.npy")
        orientation_projections_path = orientation_solver_path + "/Data/Projections"
        orientation_mean = NumpyLoader.load_numpy_arr(orientation_solver_path + "/Data/Mean/mean_img 0.npy")

        self.orientation_solver = OrientationSolver(orientation_eigenvectors, orientation_mean, orientation_solver_path, orientation_solver_num_dim)

    def init_targets(self):
        self.runtime_targets = []
        for i in range(0, len(self.crop_imgs)):
            #try:
            self.runtime_targets.append(RuntimeTarget((10,10), self.crop_img_times[i], self.crop_imgs[i], self.letter_categorizer, self.orientation_solver, self.geo_stamps, self.time_first_img_taken))
            #except:
            #    print("crashed on target img ", i, " in list")

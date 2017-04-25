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
    '''Purpose:

    1) To take the paths of the crops, load the images contained in that path. NOTE: Images need to be loaded
    case by case, or only a subset can be loaded into active memory, because it will quickly fill up. As it is now, this
    is not how it functions.

    2) Crop the images, keeping track of the x and y position of the center of the crop relative to the center of the image, as
    well as the geolocation of that full picture (through a wrapper class)

    3) Run the images for target characteristics

    4) Output target information in the desired form

    5) Submit to interop
    '''
    IMG_EXTENSION = ".JPG"
    def __init__(self, full_img_path, crop_extract_func):
        print("hi")

from SUASImageParser import Optimizer
from SUASImageParser.utils.color import bcolors
from optimizer_options import parseOptions
from optimizer_options import getOption
import cv2


# ------------------------ Creating option parser -------------------------
parseOptions()


# ------------------------ Ensuring necessary options provided ------------------------
should_exit = False
if getOption("mode") == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide a mode to use")
    should_exit = True

if getOption("output_file") == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide an output file to use")
    should_exit = True

if getOption("img_directory") == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide an image directory to use")
    should_exit = True

if should_exit:
    exit(0)

optimizer = Optimizer(img_directory=getOption("img_directory"), output_file=getOption("output_file"))

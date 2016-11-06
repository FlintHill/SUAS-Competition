from SUASImageParser import Optimizer
from SUASImageParser.utils.color import bcolors
from optimizer_options import parseOptions
from optimizer_options import getOption


# ------------------------ Creating option parser -------------------------
parseOptions()


# ------------------------ Ensuring necessary options provided ------------
should_exit = False
if getOption("mode") == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide a mode to use")
    should_exit = True

if getOption("output_directory") == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide an output directory to use")
    should_exit = True

if getOption("img_directory") == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide an image directory to use")
    should_exit = True

if should_exit:
    exit(0)

# ------------------------ Optimizing -------------------------------------
print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Beginning Optimization...")
optimizer = Optimizer(debug=True, img_directory=getOption("img_directory"), output_directory=getOption("output_directory"))
optimizer.optimize(mode="ADLC", output_directory=getOption("output_directory"), img_directory=getOption("img_directory"), multithread=True)
print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Optimization Complete!")

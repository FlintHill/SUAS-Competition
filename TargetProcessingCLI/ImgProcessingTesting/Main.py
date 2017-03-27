from PIL import Image
from ImgProcessingCLI.Testing import *
from PIL import ImageOps
import timeit

start_time = timeit.default_timer()
tester = SyntheticTester("/Users/vtolpegin/Desktop/SUAS/Generated Targets Amble/Images", "/Users/vtolpegin/Desktop/SUAS/Generated Targets Amble/Answers", 1, ".png")
print("final score: " + str(tester.get_score_vals()))
print("num crashed: " + str(tester.get_num_crashes()))
print("time elapsed: " + str(timeit.default_timer() - start_time))

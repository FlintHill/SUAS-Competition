import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("parent_dir_name + "/your_dir"")



from Classifiers.classify_color import ColorClassifier
from settings import ImgProcSettings
import json

directory = "../../image-processing/targets_new/single_targets"
answer_field = "targets.0.shape_color"
img = "8"

# test color classifier

test = ColorClassifier(directory + "/" + img + ".png")
print( test.get_color() )

# get correct answer

def str_is_int(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

p = json.load(open(directory + "_answers/" + img + ".json"))

for i in answer_field.split("."):
	if str_is_int(i):
		p = p[int(i)]
	else:
		p = p[i]

print("")
print("Loaded correct answer for " + answer_field + " which is " + str(p))


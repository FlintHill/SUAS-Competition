from PIL import Image
from pprint import pprint
import os
from UpdatedImageProcessing import *
import json
import time

DATASET_PATH = "/Users/jmoxley/Desktop/compsci/SUAS/targets_full_dataset/"
TEST_THRESHOLD = [0]
choices = ("circle", "semicircle", "quarter_circle", "triangle", "square", "rectangle", "trapezoid", "pentagon", "hexagon", "heptagon", "octagon", "star", "cross")


results = []
for x in range(len(TEST_THRESHOLD)):
    correct_answers = 0
    false_answers = 0
    data={}
    for i in range(len(choices)):
        data[choices[i]] = []
        data[choices[i]].append({
            "Correct":0,
            "Incorrect":0,
            "False Positives":0
        })
    t0 = time.time()
    for o in os.listdir(DATASET_PATH):
        if os.path.isdir(os.path.join(DATASET_PATH,o)):
            for filename in os.listdir(os.path.join(DATASET_PATH,o)):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    with open(os.path.join(DATASET_PATH,o) + "/answers/" + filename[:-4] + ".json", 'r') as f:
                        datastore = json.load(f)
                    answer = datastore["targets"][0]["shape_type"].encode("utf-8")
                    if answer == "half_circle":
                        answer = "semicircle"

                    detected = ShapeClassificationTwo(os.path.join(DATASET_PATH,o,filename)).get_shape_type()

                    if answer == detected:
                        correct_answers += 1
                        data[answer][0]["Correct"] += 1
                    else:
                        false_answers +=1
                        data[answer][0]["Incorrect"] +=1
                        data[detected][0]["False Positives"] +=1
    results.append((TEST_THRESHOLD[x], correct_answers, false_answers))
    t1 = time.time()
    print("Correct:%s Incorrect:%s" % (correct_answers, false_answers))
    pprint(data)
    print("Time taken: %s" % (t1-t0))
    print("-----------\n")

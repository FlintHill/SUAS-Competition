from PIL import Image
#from pprint import pprint
import os
from UpdatedImageProcessing import *
from alpha_trace import alpha_trace
import json


DATASET_PATH = "/Users/jmoxley/Desktop/compsci/SUAS/targets_full_dataset/"

if __name__ == "__main__":
    results = []
    for test_distance in range(RANGE[0], RANGE[1]):
        correct_answers = 0
        false_answers = 0
        data={}
        for i in range(len(choices)):
            data[choices[i]] = []
            data[choices[i]].append({
                "Correct":0,
                "Incorrect":0
            })
            for o in os.listdir(DATASET_PATH):
                if os.path.isdir(os.path.join(DATASET_PATH,o)):
                    for filename in os.listdir(os.path.join(DATASET_PATH,o)):
                        if filename.endswith(".jpg") or filename.endswith(".png"):
                            with open(DATASET_PATH + "/answers/" + filename[:-4] + ".json", 'r') as f:
                                datastore = json.load(f)
                            answer = datastore["targets"][0]["shape_type"].encode("utf-8")

                            detected = ShapeClassification(os.path.join(DATASET_PATH,o,filename))

                            if answer == detected:
                                correct_answers += 1
                                data[answer][0]["Correct"] += 1
                            else:
                                false_answers +=1
                                data[answer][0]["Incorrect"] +=1
        results.append((test_distance, correct_answers, false_answers))
        print("Min_dis:%s \nCorrect:%s Incorrect:%s" % (test_distance, correct_answers, false_answers))
        #pprint(data)
        print("-----------\n")

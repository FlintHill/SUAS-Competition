from PIL import Image
from pprint import pprint
import os
from UpdatedImageProcessing import *
from alpha_trace import alpha_trace
import json

class PeakDetectionOptimizer():

    @staticmethod
    def convert_to_shape(shape_type):
        if shape_type == "circle":
            return 0
        elif shape_type == "quarter_circle":
            return 3
        elif shape_type == "semi-circle":
            return 2
        elif shape_type == "triangle":
            return 3
        elif shape_type == "rectangle":
            return 4
        elif shape_type == "square":
            return 4
        elif shape_type == "trapezoid":
            return 4
        elif shape_type == "pentagon":
            return 5
        elif shape_type == "star":
            return 5
        elif shape_type == "hexagon":
            return 6
        elif shape_type == "heptagon":
            return 7
        elif shape_type == "octagon":
            return 8
        elif shape_type == "cross":
            return 8
        else:
            print(shape_type)
            raise Exception("Unknown shape type")

if __name__ == "__main__":

    DATASET_PATH = "/Users/jmoxley/Desktop/compsci/SUAS/test_targets"
    RANGE = (1,2)
    choices = ("circle", "semi-circle", "quarter_circle", "triangle", "square", "rectangle", "trapezoid", "pentagon", "hexagon", "heptagon", "octagon", "star", "cross")

    print("Optimizing Peak Detection...")
    print("Accessing dataset...")

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
        for filename in os.listdir(DATASET_PATH):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                with open(DATASET_PATH + "/answers/" + filename[:-4] + ".json", 'r') as f:
                    datastore = json.load(f)
                answer = datastore["targets"][0]["shape_type"].encode("utf-8")
                if answer != "circle" and answer != "quarter_circle":
                    correct_maxes = PeakDetectionOptimizer.convert_to_shape(answer)

                    canny_img = alpha_trace(os.path.join(DATASET_PATH, filename))
                    detected_maxes = len(PolarSideCounter(canny_img).get_polar_side_maximums())

                    if detected_maxes == correct_maxes:
                        correct_answers += 1
                        data[answer][0]["Correct"] += 1
                    else:
                        false_answers +=1
                        data[answer][0]["Incorrect"] +=1
        results.append((test_distance, correct_answers, false_answers))
        print("Min_dis:%s \nCorrect:%s Incorrect:%s" % (test_distance, correct_answers, false_answers))
        pprint(data)
        print("-----------\n")

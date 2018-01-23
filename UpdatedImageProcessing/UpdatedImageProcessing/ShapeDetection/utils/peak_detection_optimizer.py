from PIL import Image
from pprint import pprint
import numpy
import os
import peakutils
import math
from polar_side_counter import PolarSideCounter
from get_origin import get_origin
from alpha_trace import alpha_trace
import json

class PeakDetectionOptimizer():

    @staticmethod
    def calculate_max(canny_img, test_distance):
        loaded_img = canny_img.load()

        origin = get_origin(canny_img)
        numpy_origin = numpy.asarray(origin)

        distances = []
        angles = []
        plot = []

        for x in range(0, canny_img.size[0]):
            for y in range(0, canny_img.size[1]):
                if loaded_img[x,y] == 255:
                    distance_vector = numpy.subtract(numpy.array([x,y]), numpy_origin)
                    distance_from_origin = math.hypot(distance_vector[0], distance_vector[1])
                    distances.append(distance_from_origin)

                    angle = math.atan2(-distance_vector[1], distance_vector[0])
                    if angle < 0:
                        angle += 2*math.pi
                    angles.append(angle)

                    plot.append((angle,distance_from_origin, distance_vector))

        plotxy = sorted(plot, key=lambda a:a[0])
        plotxy = PeakDetectionOptimizer.smooth_plot(plotxy, 6, 5)

        x, y, z = zip(*plotxy)
        x=numpy.array(x)
        y=numpy.array(y)

        base = peakutils.baseline(y, 2)

        indices = peakutils.indexes(numpy.subtract(y,base), thres=0.5, min_dist=test_distance)
        return len(indices)

    @staticmethod
    def smooth_plot(plot, window, iterations):
        for i in range(0, iterations):
            for j in range(int((window-1)/2), len(plot) - int(window/2)):
                plot[j] = (plot[j][0], PeakDetectionOptimizer.get_mean_in_window(plot, j, window), plot[j][2])
        return plot

    @staticmethod
    def get_mean_in_window(plot, index, window):
        total = 0
        window_count = 0
        while window_count < window:
            total += plot[index - int(window/2) + window_count][1]
            window_count += 1
        return total/float(window)

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
    RANGE = (1,20)
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
                    detected_maxes = PeakDetectionOptimizer.calculate_max(canny_img, test_distance)

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

from ImageProcessing2 import *
import numpy
from PIL import Image
import pytesseract
import argparse
import cv2
import os

target_map_image = Image.open("/Users/zyin/Desktop/Synthetic_Dataset/Backgrounds/06150460.jpg")

total_r = 0
total_g = 0
total_b = 0
area = 0
pixel_access_target_map_image = target_map_image.load()

for x in range(target_map_image.width):
    for y in range(target_map_image.height):
        area += 1
        total_r += pixel_access_target_map_image[x, y][0]
        total_g += pixel_access_target_map_image[x, y][1]
        total_b += pixel_access_target_map_image[x, y][2]

average_r = total_r / area
average_g = total_g / area
average_b = total_b / area
average_color = (average_r, average_g, average_b)

print average_color
print ColorOperations.find_percentage_difference((38, 37, 19), average_color)

#print CannyEdgeContourDetector(target_map_image).detect_canny_edge_contours()
"""
src = raw_target_map_image
sp = 10
sr = 10
x = cv2.pyrMeanShiftFiltering(src, sp, sr)

image = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
image = Image.fromarray(image, 'RGB')
image.show()
"""

#The following code tests dynamic target detection process.
'''
target_detected = []
target_map_path = "/Users/zyin/Desktop/Synthetic_Dataset/Answers/modular_target_maps"
autonomous_image_processing_save_path = "/Users/zyin/Desktop/Target_Detection_Report"

while True:
    amount_of_target_maps_present = len(set(os.listdir(target_map_path))) - len(set(target_detected))

    while (amount_of_target_maps_present > 0):
        current_target_map_name = ""

        for index_1 in range(len(set(os.listdir(target_map_path)))):
            current_target_map_name = os.listdir(target_map_path)[index_1]

            is_current_target_map_detected = False
            for index_2 in range(len(target_detected)):
                if (target_detected[index_2] == current_target_map_name):
                    is_current_target_map_detected = True

            if (is_current_target_map_detected == False):
                target_detected.append(current_target_map_name)
                break

        combo_target_detection_result_list = SingleTargetMapDetector.detect_single_target_map(os.path.join(target_map_path, current_target_map_name))
        single_target_crops = combo_target_detection_result_list[0]
        json_file = combo_target_detection_result_list[1]

        for index_3 in range(len(single_target_crops)):
            single_target_crops[index_3].save(os.path.join(autonomous_image_processing_save_path, current_target_map_name + " - " + str(index_3 + 1) + ".png"))

        with open(os.path.join(autonomous_image_processing_save_path, current_target_map_name + ".json"), 'w') as fp:
            json.dump(json_file, fp, indent=4)

        amount_of_target_maps_present -= 1

        print amount_of_target_maps_present

    print "Run through completed"
'''

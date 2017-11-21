import json
import os.path
from TargetDetection import *
"""
mylist = TargetDetector.detect_targets("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps/1.jpg")
print mylist
#MassTargetDetector.detect_mass_target()

#SingleTargetCapturer.capture_single_target("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps/1.jpg", (3070, 2700, 3170, 2800))
"""
MassSingleTargetsCapturer.capture_mass_single_targets()

"""
json_answer_sheet = "/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps_answers/7.json"
json_data = open(json_answer_sheet)
data = json.load(json_data)

#print data["targets"][-2]["target_center_coordinates"]
print len(data["targets"][-2]["target_center_coordinates"])

j = json.loads('{"one" : "1", "two" : "2", "three" : "3"}')
#print JSONDecoder().decode("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps_answers/7.json")
print j['2']
"""

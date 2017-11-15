import json
import os.path
from TargetDetection import *

#TargetDetector(TargetDetectionSettings.TARGET_MAP_PATH, TargetDetectionSettings.TARGET_MAP_ANSWER_PATH).detect_targets()

MassTargetDetector.run_mass_target_detector()

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

import json
from ImageDetection import *
from SyntheticDataset2 import *


remaining_list = BlobDetector(ImageDetectionSettings.IMAGE_PATH, Settings.TARGET_SIZE_RANGE_IN_PIXELS).detect_blobs()
remaining_list = FalsePositiveEliminator.eliminate_overrepeated_colors("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps/2.jpg", remaining_list)
remaining_list = FalsePositiveEliminator.eliminate_overlapping_blobs(remaining_list)

print remaining_list

AutomaticTester(remaining_list, "/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps_answers/2.json").run_automatic_tester()



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

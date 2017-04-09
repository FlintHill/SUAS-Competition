import os
import json

TESTED_CROPS_DATA_PATH = "/home/robotics/Desktop/SUAS-Competition/integration_testing/data/crops/"
GENERATED_TARGETS_DATA_PATH = "/home/robotics/Desktop/SUAS-Competition/integration_testing/data/Generated_Targets/Answers"
PIXEL_DISTANCE_THRESHOLD = 30

def load_json_file(path):
    with open(path) as data_file:
        return json.load(data_file)

def load_crop_data(path):
    """
    Load a set of crops from .txt files. This method will parse the files, and
    convert the data into a dictionary format which is easy to compare with the
    generated, known data
    """
    data = {}

    for data_file_path in os.listdir(path):
        if ".txt" in data_file_path:
            name = str(data_file_path[:data_file_path.find(".")])
            data[name] = {}
            with open(os.path.join(path, data_file_path)) as data_file:
                lines = data_file.read().split()
                for line in lines:
                    line_data = line.split(":")
                    data[name][str(line_data[0])] = float(line_data[1])

    return data

def get_magnitude_of_difference(coord1, coord2):
    """
    Get the magnitude of the difference between two coordinates
    """
    diff_x = coord2[0] - coord1[0]
    diff_y = coord2[1] - coord1[1]

    return (diff_x**2 + diff_y**2)**0.5

def is_array_in_array(inner_array, outer_array):
    """
    Determine whether an inner array is in an outer array
    """
    for outer_array_object in outer_array:
        if inner_array[0] == outer_array_object[0] and inner_array[1] == outer_array_object[1]:
            return True

    return False

if __name__ == '__main__':
    # Load all images in generated targets data path
    net_score = 0.0
    false_positives = 0
    for dir_object in os.listdir(GENERATED_TARGETS_DATA_PATH):
        if ".json" in dir_object.lower():
            # Load correct image data
            generated_image_data = load_json_file(os.path.join(GENERATED_TARGETS_DATA_PATH, dir_object))
            dir_object = dir_object.split()[1]
            dir_object_crops = os.path.join(TESTED_CROPS_DATA_PATH, str(dir_object[:dir_object.find(".")]))

            # Load all generated crop data
            generated_crops_data = load_crop_data(dir_object_crops)

            # Score the parser
            image_score = 0.0
            image_false_positives = 0
            image_score_info = []
            for crop in generated_crops_data:
                print()
                print("Crop:", crop)
                false_positive = True
                crop_center_point = [generated_crops_data[crop]["center_location_x"], generated_crops_data[crop]["center_location_y"]]
                for generated_image_crop in generated_image_data:
                    center_point = generated_image_crop["midpoint"]

                    print(get_magnitude_of_difference(center_point, crop_center_point))
                    if get_magnitude_of_difference(center_point, crop_center_point) < PIXEL_DISTANCE_THRESHOLD:
                        if not is_array_in_array(center_point, image_score_info):
                            image_score_info.append(generated_image_crop["midpoint"])
                            false_positive = False

                if false_positive:
                    image_false_positives += 1

            image_score = len(image_score_info) / len(generated_image_data)
            net_score += image_score
            false_positives += image_false_positives

            print("===============================")
            print("Image Number #" + str(dir_object[:dir_object.find(".")]))
            print("Score:", image_score * 100, "%")
            print("False Positives:", image_false_positives)
            print("===============================")
            #exit(0)

    net_score = net_score / len(os.listdir(GENERATED_TARGETS_DATA_PATH))

    print("===============================")
    print("Score:", net_score * 100, "%")
    print("False Positives:", false_positives)
    print("===============================")

import os
import json

TESTED_CROPS_DATA_PATH = "/Users/vtolpegin/github/SUAS-Competition/integration_testing/data/crops"
GENERATED_TARGETS_DATA_PATH = "/Users/vtolpegin/github/SUAS-Competition/integration_testing/data/Generated_Targets"

def load_generated_target(path):
    with open(path) as data_file:
        return json.load(data_file)

def load_crop_data(path):
    """
    Load a crop from a .txt file. This method will parse the file, and convert
    the data into a dictionary format which is easy to compare with the generated
    data
    """
    pass

if __name__ == '__main__':
    # Load all images in generated targets data path
    for dir_object in os.listdir(GENERATED_TARGETS_DATA_PATH):
        if dir_object.find(".") != -1 and ".png" in dir_object.lower():
            generated_image_data = load_generated_target(os.path.join(GENERATED_TARGETS_DATA_PATH, dir_object))
            dir_object_crops = os.path.join(TESTED_CROPS_DATA_PATH, str(dir_object[:dir_object.find(".")]))

            print(generated_image_data)
            print(dir_object_crops)

            # Load all generated crops

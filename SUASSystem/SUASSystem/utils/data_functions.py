import json
import os
from jsonmerge import merge
from PIL import Image

def save_json_data(filepath, data):
    """
    Save JSON data to a file
    """
    if not os.path.exists(filepath):
        with open(filepath, 'w+') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
    else:
        loaded_data = {}
        with open(filepath) as data_file:
            loaded_data = json.load(data_file)
        compiled_data = merge(data, loaded_data)

        with open(filepath, 'w+') as outfile:
            json.dump(compiled_data, outfile, indent=4, sort_keys=True)

def crop_target(input_file_path, output_file_path, top_left_coords, bottom_right_coords):
    """
    Crop a target

    :param input_file_path: The relative path to the image to crop from
    :type input_file_path: String
    :param output_file_path: The relative path to save the cropped image to,
        including filename and type
    :type output_file_path: String
    :param top_left_coords: The top left coordinates of the crop in the original
        image
    :type top_left_coords: [int, int]
    :param bottom_right_coords: The bottom right coordinates of the crop in the
        original image
    :type bottom_right_coords: [int, int]
    """
    input_image = Image.open(input_file_path)
    bound_box = (top_left_coords[0], top_left_coords[1], bottom_right_coords[0], bottom_right_coords[1])

    cropped_image = input_image.crop(bound_box).convert("RGB")
    cropped_image.save(output_file_path)

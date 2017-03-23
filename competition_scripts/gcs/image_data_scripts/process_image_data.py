import json

SAVE_COORDINATES_PATH = "./location_mission_data.json"
IMAGE_PATH = "./images"

def load_location_data(path):
    with open(data_file_path, 'r') as infile:
        return json.load(infile)

def load_images(path):
    pass

def match_test_images_with_location_data(images, location_data):
    pass

def match_image_with_closest_location_data(image, location_data):
    pass

def save_matched_data(matched_data):
    pass

if __name__ == '__main__':
    location_data = load_location_data(SAVE_COORDINATES_PATH)
    images = load_images(IMAGE_PATH)

    matched_data = match_test_images_with_location_data(images, location_data)

    save_matched_data(matched_data)

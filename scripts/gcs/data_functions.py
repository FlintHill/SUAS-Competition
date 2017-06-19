import json
import os
from jsonmerge import merge

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

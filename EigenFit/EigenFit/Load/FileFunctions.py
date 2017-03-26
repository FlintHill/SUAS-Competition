import os
from PIL import Image

def get_paths_with_extension(path, extension):
    names = os.listdir(path)
    remove_names_without_extension(names, extension)
    for i in range(0, len(names)):
        names[i] = path + "/" + names[i]
    return names

def remove_names_without_extension(file_names, extension):
    i = 0
    while i < len(file_names):
        if not file_names[i].endswith(extension):
            del file_names[i]
        else:
            i += 1

def get_max_filepath(base_dir):
    files = os.listdir(base_dir)
    max_file = max(files)
    return base_dir + "/" + max_file

def remove_dirs_that_arent_folders(dirs):
    i = 0
    while i < len(dirs):
        if os.path.isfile(dirs[i]):
            del dirs[i]
        else:
            i+=1

def load_imgs(img_paths):
    imgs = []
    for i in range(0, len(img_paths)):
        imgs.append(Image.open(img_paths[i]).convert('L'))
    return imgs

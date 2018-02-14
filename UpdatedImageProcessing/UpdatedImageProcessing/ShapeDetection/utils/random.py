import random

def get_random_img_color(img, image):
    x = random.randint(0, img.size[0] - 1)
    y = random.randint(0, img.size[1] - 1)
    return image[x,y]

def get_random_value_from_list(list_in, exclusions = []):
    if len(exclusions) == 0:
        index = random.randint(0, len(list_in)-1)
        return list_in[index]
    end = False
    while end == False:
        index = random.randint(0, len(list_in)-1)
        if not list_in[index] in exclusions:
            end = True
            return list_in[index]

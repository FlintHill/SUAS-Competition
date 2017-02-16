import random


def get_random_img_color(img, image):
    x = random.randint(0, img.size[0] - 1)
    y = random.randint(0, img.size[1] - 1)
    return image[x,y]

def get_random_value_from_list(list_in):
    index = random.randint(0, len(list_in)-1)
    print("random: " + str(list_in[index]))
    return list_in[index]
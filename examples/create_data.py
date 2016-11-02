import cv2
import numpy as np
from SUASImageParser.utils.color import bcolors
from create_data_options import parseOptions
from create_data_options import getOption
import os
import json

parseOptions()

Path = getOption("image")
output = getOption("output_directory")
should_exit = False
if Path == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide an image to use")
    should_exit = True

if output == None:
    print(bcolors.FAIL + "[Error]" + bcolors.ENDC + " Please provide an output directory to use")
    should_exit = True

if should_exit:
    exit(0)

if not os.path.exists(output):
    os.mkdir(output)

image_float_size = 1150.0
image_int_size = int(image_float_size)
color = [0,255,0]
rectangle = False
obj_index = 1

def on_event(event,x,y,flags,param):
    global draw_image
    global startpointx,startpointy,rectangle
    global x_scale, y_scale
    global image
    global obj_index

    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle = True
        startpointx = x
        startpointy = y
        draw_image = resized.copy()
        cv2.rectangle(draw_image,(x,y),(x,y),(0,255,0))

    elif event == cv2.EVENT_LBUTTONUP:
        rectangle = False
        draw_image = resized.copy()
        area = {
            "x_start" : int(x_scale * startpointx),
            "y_start" : int(y_scale * startpointy),
            "x_finish" : int(x_scale * x),
            "y_finish" : int(y_scale * y)
        }
        with open(output + str(obj_index) + ".txt", 'w+') as output_f:
            json.dump(area, output_f)
        obj_index += 1
        print('Target successfully saved')

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle:
            draw_image = resized.copy()
            cv2.rectangle(draw_image,(startpointx,startpointy),(x,y),(0,255,0))

# Read the image and convert it into gray
image = cv2.imread(Path)
cv2.imwrite(output + "image.jpg", image)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# resize the image
ration = image_float_size / gray_image.shape[1]
dim = (image_int_size,int(gray_image.shape[0]*ration))
y_scale = image.shape[0] / dim[1]
x_scale = image.shape[1] / dim[0]
resized = cv2.resize(gray_image, dim, interpolation = cv2.INTER_AREA)
draw_image = resized.copy()

# set window for the image
cv2.namedWindow('window')

# mouse callback
cv2.setMouseCallback('window',on_event)

while True:
    cv2.imshow('window', draw_image)
    ch = 0xFF & cv2.waitKey(1)
    if ch == 27:
        break

cv2.destroyAllWindows()

from PIL import Image
import cv2
import numpy
import collections


def alpha_trace(file_path):
    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

    pil_img = Image.open(file_path)
    cvimg = numpy.array(pil_img)

    pil_output = Image.new("L", (pil_img.width, pil_img.height))
    output_img = numpy.array(pil_output)

    rows = pil_img.width - 1
    columns = pil_img.height - 1

    for i in range(1,columns):
        for j in range(1,rows):
            if(compare(cvimg[i][j],[255,255,255,0])):
                output_img[i][j] = 0
            else:
                if(compare(cvimg[i-1][j],[255,255,255,0]) or compare(cvimg[i][j-1],[255,255,255,0])):
                    output_img[i][j] = 255
                elif(compare(cvimg[i+1][j],[255,255,255,0]) or compare(cvimg[i][j+1],[255,255,255,0])):
                    output_img[i][j] = 255
                else:
                    output_img[i][j] = 0
    return Image.fromarray(output_img)

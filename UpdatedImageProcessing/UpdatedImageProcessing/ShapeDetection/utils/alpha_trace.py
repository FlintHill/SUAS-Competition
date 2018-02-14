from PIL import Image
import cv2
import numpy

def alpha_trace(file_path):
    pil_img = Image.open(file_path)
    cvimg = numpy.array(pil_img)

    pil_output = Image.new("L", (pil_img.width, pil_img.height))
    output_img = numpy.array(pil_output)

    rows = pil_img.width - 1
    columns = pil_img.height - 1

    for i in range(1,columns):
        for j in range(1,rows):
            if(cvimg[i][j][3] == 0):
                output_img[i][j] = 0
            else:
                if(cvimg[i-1][j][3] == 0 or cvimg[i][j-1][3] == 0):
                    output_img[i][j] = 255
                elif(cvimg[i+1][j][3] == 0 or cvimg[i][j+1][3] == 0):
                    output_img[i][j] = 255
                else:
                    output_img[i][j] = 0
    return Image.fromarray(output_img)

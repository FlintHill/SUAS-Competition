from PIL import Image
import numpy

def alpha_fill(pil_img):
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
                output_img[i][j] = 255

    return output_img

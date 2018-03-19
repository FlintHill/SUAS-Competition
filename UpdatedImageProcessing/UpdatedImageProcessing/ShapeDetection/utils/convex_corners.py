import cv2
from alpha_fill import alpha_fill
import numpy


def convex_corners(pil_img, show_plot=False):
    mask_img = alpha_fill(pil_img)

    _,contours,_ = cv2.findContours(mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[0]

    hull = cv2.convexHull(contour,returnPoints = False)
    defects = cv2.convexityDefects(contour,hull)

    if show_plot:
        mask_img = cv2.cvtColor(mask_img, cv2.COLOR_GRAY2RGB)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            cv2.line(mask_img,start,end,[0,255,0],2)
            cv2.circle(mask_img,far,5,[0,0,255],-1)
        cv2.imshow('img',mask_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return defects.shape[0]

def convex_corners_cross(pil_img, show_plot=False):
    mask_img = alpha_fill(pil_img)

    _,contours,_ = cv2.findContours(mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[0]

    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = numpy.int0(box)

    hull = cv2.convexHull(contour,returnPoints = False)
    print(hull)
    defects = cv2.convexityDefects(contour,box)


    mask_img = cv2.cvtColor(mask_img, cv2.COLOR_GRAY2RGB)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        cv2.line(mask_img,start,end,[0,255,0],2)
        cv2.circle(mask_img,far,5,[0,0,255],-1)
    cv2.imshow('img',mask_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

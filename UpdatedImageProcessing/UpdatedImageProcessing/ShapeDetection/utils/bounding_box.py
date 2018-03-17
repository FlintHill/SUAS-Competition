import cv2
import numpy
from alpha_fill import alpha_fill

class BoundingBox(object):

    def __init__(self, pil_img, show_plot=False):
        self.mask_img = alpha_fill(pil_img)
        self.set_bounding_box()
        self.set_side_lengths()

        self.set_areas()

        if show_plot:
            self.show_plot()

    def set_bounding_box(self):
        _,contours,_ = cv2.findContours(self.mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        self.contour = contours[0]

        rect = cv2.minAreaRect(self.contour)
        self.box = cv2.boxPoints(rect)
        #self.box = numpy.int0(box)

    def set_side_lengths(self):
        point1 = self.box[0]
        point2 = self.box[1]
        point3 = self.box[2]

        diffx = numpy.abs(point1[0]-point2[0])
        diffy = numpy.abs(point1[1]-point2[1])
        side1 = numpy.hypot(diffx,diffy)

        diffx = numpy.abs(point2[0]-point3[0])
        diffy = numpy.abs(point2[1]-point3[1])
        side2 = numpy.hypot(diffx,diffy)

        self.bounding_box_side_lengths = (side1,side2)

    """
    def set_areas(self):
        self.hull = cv2.convexHull(self.contour)
        self.unpacked_hull = []
        for i in range(len(self.hull)):
            self.unpacked_hull.append((self.hull[i][0][0],self.hull[i][0][1]))

        self.hull_area = self.polygon_area(self.unpacked_hull)
        self.bounding_box_area = self.bounding_box_side_lengths[0]*self.bounding_box_side_lengths[1]
    """

    def set_areas(self):
        epsilon = 0.001*cv2.arcLength(self.contour,True)
        self.contour_approx = cv2.approxPolyDP(self.contour,epsilon,True)
        self.unpacked_contour_approx = []
        for i in range(len(self.contour_approx)):
            self.unpacked_contour_approx.append((self.contour_approx[i][0][0],self.contour_approx[i][0][1]))

        self.contour_approx_area = self.polygon_area(self.unpacked_contour_approx)
        self.bounding_box_area = self.bounding_box_side_lengths[0]*self.bounding_box_side_lengths[1]

    def show_plot(self):
        color_img = cv2.cvtColor(self.mask_img, cv2.COLOR_GRAY2RGB)
        #cv2.drawContours(color_img,self.hull,0,(0,0,255),4)

        cv2.drawContours(color_img,[self.contour_approx],0,(0,0,255),1)
        cv2.drawContours(color_img,[numpy.int0(self.box)],0,(0,255,0),1)
        cv2.imshow('image',color_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_box(self):
        return self.box

    def get_side_lengths(self):
        return self.bounding_box_side_lengths

    def get_side_length_difference(self):
        return numpy.abs(side_lengths[0]-side_lengths[1])

    def get_area_difference(self):
        return numpy.abs(self.contour_approx_area-self.bounding_box_area)

    def polygon_area(self, corners):
        n = len(corners)
        cx = float(sum(x for x, y in corners)) / n
        cy = float(sum(y for x, y in corners)) / n
        cornersWithAngles = []
        for x, y in corners:
            an = (numpy.arctan2(y - cy, x - cx) + 2.0 * numpy.pi) % (2.0 * numpy.pi)
            cornersWithAngles.append((x, y, an))
        cornersWithAngles.sort(key = lambda tup: tup[2])
        corners = map(lambda (x, y, an): (x, y), cornersWithAngles)

        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += corners[i][0] * corners[j][1]
            area -= corners[j][0] * corners[i][1]
        area = abs(area) / 2.0
        return area

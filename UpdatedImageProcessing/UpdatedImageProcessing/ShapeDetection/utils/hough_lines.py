import numpy
import cv2

class HoughSideCounter(object):

    def __init__(self, img, canny_img, threshold, show_plot=False):
        self.img = img
        self.canny_img = numpy.array(canny_img)
        self.threshold = threshold

        self.sides = self.side_counter()

        if show_plot:
            self.plot_lines()

    def side_counter(self):
        rho = 1
        theta = numpy.pi/180

        lines = cv2.HoughLines(self.canny_img, rho, theta, self.threshold)
        sides = []
        if type(lines) == "NoneType":
            return 0
        else:
            for i in range(len(lines)):
                hl = HoughLine(lines[i])

                if len(sides) == 0:
                    sides.append(hl)

                else:
                    unique_line = True
                    for i in range(len(sides)):
                        if abs(sides[i].get_theta() - hl.get_theta()) < 0.5:
                            if abs(sides[i].get_rho() - hl.get_rho()) < 50:
                                unique_line = False
                                break
                    if unique_line:
                        sides.append(hl)
            return sides

    def plot_lines(self):
        for i in range(len(self.sides)):
            points = self.sides[i].get_plot_points()
            cv2.line(self.img,points[0],points[1],(0,0,255),2)

        cv2.imshow('image',self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_sides(self):
        return self.sides

class HoughLine(object):
    def __init__(self, lines_array):
        self.lines_array = lines_array
        self.set_points()

    def set_points(self):
        for rho,theta in self.lines_array:
            self.rho = rho
            self.theta = theta

            a = numpy.cos(theta)
            b = numpy.sin(theta)
            x0 = a*rho
            y0 = b*rho
            self.x1 = int(x0 + 1000*(-b))
            self.y1 = int(y0 + 1000*(a))
            self.x2 = int(x0 - 1000*(-b))
            self.y2 = int(y0 - 1000*(a))

    def get_plot_points(self):
        return ((self.x1,self.y1),(self.x2,self.y2))

    def get_rho(self):
        return self.rho

    def get_theta(self):
        return self.theta

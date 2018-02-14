import numpy
from EigenFit.Vector import *

class NamedProjections(object):

    def __init__(self, name, projections):
        self.name = name
        self.projections = projections
        self.init_mean()

    def init_mean(self):
        self.mean = numpy.mean(self.projections, axis=0)

    def get_name(self):
        return self.name

    def get_projections(self):
        return self.projections

    def get_mean(self):
        return self.mean

    def get_unit_mean(self):
        return unit_vector(self.mean)

    def __repr__(self):
        return self.name

'''
Created on Jan 27, 2017

@author: phusisian
'''
from ObjAvoid import MassHolder
from ObjAvoid import DroneMass
from ObjAvoid import MultiDimPoint
from .current_coordinates import CurrentCoordinates
from math import sin, cos

class ClientConverter(object):

    '''initialCoordinates will be current_coordinates from client class'''
    '''the role of the class is to funnel data from the client script into forms that are usable with my code.
    currently updates the position of the drone mass, but is set up to update other masses as well if it were
    to be funneled them fairly simply'''
    def __init__(self, initialCoordinatesIn):
        self.massHolder = MassHolder()
        self.initialCoordinates = initialCoordinatesIn
        self.initMainDroneMass()


    def getInitialCoordinates(self):
        return self.initialCoordinates


    def initMainDroneMass(self):
        self.mainDroneMass = DroneMass(self.massHolder, MultiDimPoint([0,0,self.initialCoordinates[2]]), DroneMass.DEFAULT_DRONE_MASS)


    ''''needs to take coordinates in list that includes: altitude, haversine distance, and heading,
    (in this order: haversine distance, heading, altitude)
    with haversine distance and bearing calcuated from ClientConverter's initial coordinates, which can be pulled
    from "getInitialCoordinates()"'''
    def updateMainDroneMass(self, updateData):
        dy = updateData[0] * sin(updateData[1])#where DY is change in y from initial GPS point
        dx = updateData[0] * cos(updateData[1])#where DX is change in x from initial GPS point
        newDronePoint = MultiDimPoint([dy, dx, updateData[2]])
        self.mainDroneMass.setPoint(newDronePoint)


    '''reminder not to switch to guided mode unless tgher are nearby obstacles nearby. Search all the masses
    in massHolder to see if any are close enough that they should be avoided'''

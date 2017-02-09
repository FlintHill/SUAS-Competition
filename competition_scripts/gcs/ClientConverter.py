'''
Created on Jan 27, 2017

@author: phusisian
'''
from ObjAvoid import MassHolder
from ObjAvoid import DroneMass
from ObjAvoid import MultiDimPoint
from current_coordinates import CurrentCoordinates
from math import sin, cos

class ClientConverter(object):

    '''initialCoordinates will be CurrentCoordinates object'''
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
        self.mainDroneMass = DroneMass(self.massHolder, MultiDimPoint([0,0,self.initialCoordinates.get_altitude()]), DroneMass.DEFAULT_DRONE_MASS)


    def setWaypoints(self, waypointsIn):
        

    '''takes an converter_data_update object that wraps altitude, haversine distance, and heading from the current position
    to the position the drone needs to travel.
    
    '''
    def updateMainDroneMass(self, updateData):
        dy = updateData.get_haversine_distance() * sin(updateData.get_heading())#where DY is change in y from initial GPS point
        dx = updateData.get_haversine_distance() * cos(updateData.get_heading())#where DX is change in x from initial GPS point
        newDronePoint =  MultiDimPoint([dy, dx, updateData.get_altitude()])
        self.mainDroneMass.setPoint(newDronePoint)


    '''reminder not to switch to guided mode unless there are nearby obstacles nearby. Search all the masses
    in massHolder to see if any are close enough that they should be avoided'''

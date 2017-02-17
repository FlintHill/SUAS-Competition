'''
Created on Jan 10, 2017

@author: phusisian
@author: vtolpegin
'''
from ObjAvoid import MultiDimPoint
from ObjAvoid import Vector
from ObjAvoid import Mass
from ObjAvoid import MassHolder
from ObjAvoid import DroneMass
from time import sleep
from ObjAvoid import RandomPointMaker

waypoints = [MultiDimPoint([10, 10]), MultiDimPoint([15, 15])]
massHolder = MassHolder()
droneMass = DroneMass(massHolder, MultiDimPoint([0,0]), 1, waypoints)
massHolder.appendDroneMass(droneMass)

randomPointMaker = RandomPointMaker(2, ((-700, 700), (-500, 500)))
for i in range(0, 10):
    randPoint = randomPointMaker.createRandomPoint()
    mass = Mass(massHolder, randPoint, 500)
    massHolder.appendMass(mass)

while True:
    massHolder.tick()
    print(massHolder)
    sleep(1)

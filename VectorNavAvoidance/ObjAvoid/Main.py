'''
Created on Jan 10, 2017

@author: phusisian
@author: vtolpegin
'''
from MultiDimPoint import MultiDimPoint
from Vector import Vector
from Mass import Mass
from MassHolder import MassHolder
from DroneMass import DroneMass
from time import sleep
from RandomPointMaker import RandomPointMaker

massHolder = MassHolder()
droneMass = DroneMass(massHolder, MultiDimPoint([0,0]), 1)
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

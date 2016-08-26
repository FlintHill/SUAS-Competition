Mission Planner
===============

This is the control software for the drone. Because of a few different objectives this year the source will have to be modified to work with the following:

#. Add obstacles (SDA).
   Spheres will be used for moving obstacles and cylinders will be used for stationary obstacles. For each obstacle, if it is stationary, the drone should move around it. However, if the obstacle is moving, then the drone should either get out of its way (if it is approaching the drone) or wait for the obstacle to leave before proceeding to continue to the next waypoint.
#. Air drop.
   Mission Planner will need to autonomously determine when to drop the payload and then drop the payload without any manual input (except an OK signal that the drone is allowed to drop whenever it sees fit)

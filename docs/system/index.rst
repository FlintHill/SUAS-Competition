System
======

The system is broken down into numerous parts. The architecture for the system as a whole is as follows:

.. image:: ../_static/suas_system_arch.png

Each section in the above image will be discussed in more detail in the following pages.

#. :doc:`system/hardware`.
   Understanding the hardware is a key requirement before being able to successfully develop with the system.
#. :doc:`system/navio2`.
   The NAVIO2 is the brain of the of drone and combines both hardware and software aspects from the competition.
#. :doc:`system/tx1`.
   The TX1 completes all image processing onboard the drone.
#. :doc:`system/missionplanner`.
   Ground Control Station software for controlling the drone.
#. :doc:`system/mp`.
   This is a script which runs within MissionPlanner that interfaces with the interoperability client to both send and receive data from the interoperability server.
#. :doc:`system/tra`.
   The Target Recognition Application is in charge of submitting targets to the interoperability server.
#. :doc:`system/interoperabilityclient`.
   This allows the TRA and MP scripts to communicate with the interoperability server.

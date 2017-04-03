SDA VIEWER Explanation
======================
This application allows us to view, from any web browser, the current 
set of obstacles and the drone's position via websockets in realtime. 

About
-----
DESCRIPTION OF WHY THIS IS REQUIRED.

This is used by Flint Hill's Animus Ferus Team in the SUAS Competition.

WebSocket Server Specification
------------------------------
This section regards the information that needs to be transmitted from
a WebSocket server in order to be used in the viewer.

The following information is *required* for the viewer to operate:
 1. The drone's
   - Latitude,
   - Longitude,
   - Altitude, and
   - Bearing.
 2. Transmitted in a JSON format.
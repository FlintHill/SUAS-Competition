# SDA VIEWER

This page details the setup, function, and operation of the Sense, Detect, and Avoid viewer.

## Viewer

This application allows us to view, from any modern web browser, the current 
set of obstacles and the drone's position via websockets in realtime.

The details of the program are enumerated below.

### About

Using a combination of an [Apache webserver](https://www.apache.org/) with a [PHP](https://php.net/) extension and a [MySQLi library](https://php.net/manual/en/book.mysqli.php) included, [MySQL database](https://www.mysql.com/), Javascript with [JQuery](https://jquery.com/) and [LeafletJS](http://leafletjs.com/) libraries inlcuded, we have created viewer that allows e

DESCRIPTION OF WHY THIS IS REQUIRED.

This is used by Flint Hill's Animus Ferus Team in the AUVSI SUAS Competition.

### Setup and Configuration

The rough instructions on how to start up and configure the viewer are detailed below:

1. Download and install:
	- Apache 2.4
	- PHP 7
	- MySQL
	- 


### Interop. Server Specification

This section details the exact information retrieved from the AUVSI SUAS' Interoperability Server, based off the specifications that they detail here: 

http://auvsi-suas-competition-interoperability-system.readthedocs.io/en/latest/specification.html



### WebSocket Server Specification

This section regards the information that needs to be transmitted from
a WebSocket server in order to be used in the viewer.

A websocket is the second and last connection that the viewer needs to establish in order to obtain the drone's current position, as it cannot be obtained elsewhere.

An **example of the response** that a websocket might return is displayed below:

```
{
    "alt": 100,
    "dir": 123.45,
    "speed": 0.0,
    "lat": 38.870373038,
    "long": -77.319760077
}
```

**Note:** The the response is just a simple collection of JSON elements, not an array.

The information, mych like the example response above, is retrieved after a dummy message is sent to the websocket, where the websocket then returns the information immediately afterwards.

The following information is **required** for the viewer to operate:

| Short | Full Field Name | Type              | Description |
| :---- | :-------------- | :---------------- | :---------- |
| alt   | Altitude        | (Integer) Decimal | Absolute distance from the ground, not sea level, to the drone. |
| dir   | Direction       | _same as above_   | In degrees, from 0 to 360 inclusive, where the drone is pointing to relative to the north pole. |
| speed | Speed           | _same as above_   | The change, or delta, in the drone's current latitude and longitude from it's last. |
| lat   | Latitude        | _same as above_   | The difference from the equator to the drone's current latitude in decimal degrees.
| long  | Longitude       | _same as above_   | The difference from the Prime Meridian to the drone's current longitude in decimal degrees. |

All of this information, except altitude, is critical in displaying the drone's current position.

### Features not yet implemented

Currently, the altitude is not taken into account with regards to obstacles. If an obstacle does not exist on the same altitude as the drone, then ideally, the obstacle would be made either semi or fully transparent. This is a feature that needs to implemented at a later date.

## Tile Server

# rsc/js Breakdown

This page describes the resources that are used in the Sense, Detect, and Avoid visualizer, as well as documentation for the script that handles the viewer.

## Resources

| Resource            | Friendly-resource-name        | Description  |
| :-                  |:-             | -         |
| html5shiv.js        | [aFarkas/html5shiv](https://github.com/aFarkas/html5shiv) | Enables HTML5 compatibility with outdated browsers, such as Internet Explorer. |
| jquery.3.1.1.min.js | [JQuery](https://jquery.com/) | Provides convenience functions that simplifies certain tasks like updating the viewer. |
| leaflet.min.js      | [LeafletJS](http://leafletjs.com/reference-1.0.3.html) | Loads in map tiles and displays them in the background of the viewer page. |
| images/             | LeafletJS icons      | Icons that may be used in LeafletJS. |
| main.3.js           | FlintHill/SUAS-Competition      | The script that connects to the Websocket server, then handles and displays the server data onto the webpage. |

**Note:** main.2.js and main.1.js are outdated versions of the main script that are kept in the resources directory as a backup, and to remember the initial code that ran the viewer.

## main.3.js

### EssentialsContainer _class_

> Contains all the essential functions needed throughout the rest of this script and other console-based commands.

The following are the static functions that are included within the class:

__sleep__(_int_ millisecond)

Pauses the execution of the script for a specificed amount of time.

| Variable name | Type | Description  |
| :------------ |:---- | :---- |
| milliseconds  | int  | number of milliseconds to pause execution for. |

__Returns:__ nothing.

__screwMeUp__()

Function with unforseen use.

__Returns:__ nothing.

__rips__()

Toggles the visibility of the SDA viewer description and explanation. By
default, the aforementioned information is not displayed for convenience.

__Returns:__ nothing.

***

### DataConverters _class_

Depends on: LeafletJS

> Converts data, which is assumed to be an array of JSON elements, where each elements contains a field named "latitude" and "longitude", like so:

The following are the static functions that are included within the class:

__line__(_Array_ data, _String_ color, _boolean_ marker, _String_ \_title, _Variable_ \_icon)

| Variable name | Type     | Description  |
| :------------ |:-------- | :---- |
| data          | Array    | Array where indexes are arrays with two elements: lat, lng. |
| color         | String   | Specifies the color of the line. Examples: 'red', 'green', 'blue', 'purple', and etc. |
| marker        | boolean  | Whether or not points are added to the line. If (markers) is true, this function returns an array with two elements: line, and marker. |
| \_title       | String   | If marker is true: specifies the hover text. |
| \_icon        | Variable | If marker is true: the icon that appears on the markers. |

__marker__(_Array_ data, _String_ \_title, _Variable_ \_icon)

| Variable name | Type     | Description  |
| :------------ |:-------- | :---- |
| data          | Array    | Array where indexes are arrays with two elements: lat, lng. |
| \_title       | String   | If marker is true: specifies the hover text. |
| \_icon        | Variable | If marker is true: the icon that appears on the markers. |

__circle__(_Array_ data, _boolean_ marker, _Double_ \_radius, _String_ \_color, _String_ \_title)

***

### LeafletInterface _class_

> Is used by the WebsocketHandler class to interact with the LeafletJS map.

The following is the static function that is included within the class:

__markersDo__(_String_ action)

Primarily, the action String of "remove" will be used. "clear" is not expected to be implemented in any use case.

TODO correct.

***

### WebsocketHandler _class_

TODO expand.

***

### WebsocketControls _class_

TODO expand.



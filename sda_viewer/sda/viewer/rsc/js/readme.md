# rsc/js Breakdown

This page describes the resources that are used in the Sense, Detect, and Avoid visualizer, as well as documentation 

## Resources

| Resource            | Friendly-resource-name        | Description  |
| :-                  |:-             | -         |
| html5shiv.js        | [aFarkas/html5shiv](https://github.com/aFarkas/html5shiv) | Enables HTML5 compatibility with outdated browsers, such as Internet Explorer. |
| jquery.3.1.1.min.js | [JQuery](https://jquery.com/) | Provides convenience functions that simplifies certain tasks like updating the viewer. |
| leaflet.min.js      | [LeafletJS](http://leafletjs.com/reference-1.0.3.html) | Loads in map tiles and displays them in the background of the viewer page. |
| images/             | LeafletJS icons      | Icons that may be used in LeafletJS. |
| main.3.js           | FlintHill/SUAS-Competition      | The script that connects to the Websocket server, then handles and displays the server data onto the webpage. |

## main.3.js

### EssentialsContainer _class_

The following are the static functions that are included within the class:

__sleep__(_int_ millisecond)

Pauses the execution of the script for a specificed amount of time.

| Variable name | Type | Description  |
| :------------ |:---- | :---- |
| milliseconds  | int  | number of milliseconds to pause execution for. |

__Returns:__ nothing.

TODO finish.

***

### DataConverters _class_

TODO expand.

***

### LeafletInterface _class_

TODO expand.

***

### WebsocketHandler _class_

TODO expand.

***

### WebsocketControls _class_

TODO expand.



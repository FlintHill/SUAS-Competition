/**
 * SDA Viewer Main Script
 * ===
 * This is the javascript file the contains all the code necessary to operate
 * the viewer. The code's functions are as follows:
 *
 * 	- Initialize a LeafletJS map that loads tiles from a local server.
 *  - Handle the User Interface in the browser.
 * 	- Connect to the SDA Viewer websocket.
 * 	- Add and update relevant points, such as drone position, obstacles, and
 * 	  more to the LeafletJS map.
 *
 * This code depends on, but doesn't necessarily check for:
 * 	- JQuery (version >= 3.1.1)
 *
 * @author		James Villemarette
 * @version		3.0
 * @since		2016-04-21
 */

class EssentialsContainer {

	/**
	 * EssentialsContainer class
	 *
	 * Contains all the essential functions needed throughout the rest of this
	 * script and other console-based commands.
	 */

	/**
	 * sleep(int millisecond)
	 *
	 * Pauses the execution of the script for a specificed amount of time.
	 *
	 * @param	milliseconds	number of milliseconds to pause execution for.
	 * @returns					nothing.
	 */
	static sleep(milliseconds) {

		var start = new Date().getTime();
		for (var i = 0; i < 1e7; i++) {
			if ((new Date().getTime() - start) > milliseconds){
				break;
			}
		}

	};

	/**
	 * screwMeUp()
	 *
	 * Function with unforseen use.
	 *
	 * @returns		nothing.
	 */
	static screwMeUp() {

		$.when($.when($.when($.when($.when().then()).then()).then()).then()).
			then(console.log("shamrock shakes"));
		return null;

	};

	/**
	 * rips()
	 *
	 * Toggles the visibility of the SDA viewer description and explanation. By
	 * default, the aforementioned information is not displayed for convenience.
	 *
	 * @returns		nothing.
	 */
	static rips() {
		if( $("#information").css("display") == "block" ) {
			$("#information").css("display", "none");
			$("#dropdown").text("Show Description"); // &uarr;
		} else {
			$("#information").css("display", "block");
			$("#dropdown").text("Show Description"); // &darr;
		}
	};

}

class DataConverters {

	/**
	 * DataConverters class
	 * Depends on: LeafletJS
	 *
	 * Converts data, which is assumed to be an array of JSON elements, where
	 * each elements contains a field named "latitude" and "longitude", like so:
	 *
	 *	"boundary_pts": [
	 *		{
	 *			"latitude": 38.142544,
	 *			"longitude": -76.434088,
	 *      },
	 *		{
	 *			"latitude": 38.141833,
	 *			"longitude": -76.425263,
	 *		},
	 *		{
	 *			"latitude": 38.144678,
	 *			"longitude": -76.427995,
	 *		}
	 *	]
	 *
	 * to a Leaflet Marker, Line, both, or a circle.
	 */

	/**
	 * line(Array data, String title, String _color, Boolean marker,
	 *	String _title, Variable _icon)
	 *
	 * @param	data 	array where indexes are arrays with two elements:
	 *					lat, lng.
	 * @param	_color	specifies the color of the line.
	 *	- examples: 'red', 'green', 'blue', 'purple', and etc.
	 *
	 * @param	marker 	whether or not points are added to the line.
	 *  - if (markers) is true, this function returns an array with two
	 *	  elements: line, and marker.
	 *
	 * @param	_title	if marker is true: specifies the hover text.
	 * @param	_icon 	if marker is true: the icon that appears on the markers.
	 * @returns			A Leaflet polyline if marker is false, or an array
	 *					containing a Leaflet polyline and Leaflet markers if
	 *					marker is true.
	 */
	static line(data, _color, marker, _title, _icon) {

		var latlngs = [], points = [];

		for(var i = 0; i < data.length; i++) {
			var point = [data[i].latitude, data[i].longitude];

			if(marker)
				points[i] = L.marker(point, {icon: _icon, title: _title + ' #' +
					data[i].order});

			latlngs.push(point);
		}

		if(marker)
			return [L.polyline(latlngs, {color: _color, interactive: false})].concat(points);
		else
			return L.polyline(latlngs, {color: _color, interactive: false});

	}

	/**
	 * marker(Array data, String title, Variable icon)
	 *
	 * @param	data 	Array with two indexes, [0] being lat., [1] being long.
	 * @param	_title	specifies the hover text.
	 * @param	_icon 	the icon that appears on the markers.
	 * @returns			A Leaflet marker.
	 */
	static marker(data, _title, _icon) {

		return L.marker(
			[data.latitude, data.longitude],
			{icon: _icon, title: _title}
		);

	}

	/**
	 * circle(Array data, String _color, String _title)
	 *
	 * @param	data 	Array with two indexes, [0] being lat., [1] being long.
	 * @param	marker 	If true, the marker is fixed to a 10 pixel radius.
	 * @param	_radius	the radius of the circle in meters. if -1, the radius is
	 *					grabbed from data, assuming a field named "radius" is
	 *					included with each data point.
	 * @param	_title	specifies the hover text.
	 * @returns			A Leaflet circle.
	 */
	// TODO: cleanup, too much redundant code
	static circle(data, marker, _radius, _color, _title) {

		var circles = [];

		for(var i = 0; i < data.length || marker; i++) {

			if(marker) {
				return L.circleMarker([data.latitude, data.longitude]);
			} else {
				if(_radius == -1)
					circles.push(
						L.circle([data[i].latitude, data[i].longitude],
							{radius: (data[i].cylinder_radius * 0.305),
							color: _color,
							title: _title}
						)
					);
				else
					circles.push(
						L.circle([data[i].latitude, data[i].longitude],
						{radius: _radius, color: _color, title: _title})
					);
			}

		}

		return circles;

	}

}

// Leaflet Interface Variables
var leafletData = {

	// mission waypoints
	waypoints_points: [],
	waypoints_line: null,
	waypoints_latlngs: [],

	// search grid
	search_grid_points: [],
	search_grid_line: null,
	search_grid_latlngs: [],

	// flight zone
	fly_zone_line: null,
	fly_zone_latlngs: [],

	// points
	air_drop_pos_point: null,
	emergent_last_know_pos_point: null,
	home_pos_point: null,
	off_axis_target_pos_point: null,

	// circles and special points
	obstacles_circles: [],
	drone_pos_point: null,

	// utility functions
	do: function(action, map) {
		var keys = Object.keys(this);

		for(var i = 0; i < keys.length; i++) {

			switch(action) {
				case "clear":

					if(this[keys[i]] instanceof Array)
						this[keys[i]].length = 0;
					else if(!(this[keys[i]] instanceof Function))
						this[keys[i]] = null;

					break;
				case "addTo":

					if(this[keys[i]] == null || this[keys[i]] == [])
						break;

					if(this[keys[i]] instanceof Array)
						this[keys[i]].forEach(function(element) { element.addTo(map); });
					else if(!(this[keys[i]] instanceof Function))
						this[keys[i]].addTo(map);

					break;
				case "remove":

					if(this[keys[i]] == null || this[keys[i]] == [])
						break;

					if(this[keys[i]] instanceof Array)
						this[keys[i]].forEach(function(element) {
							mymap.removeLayer(element);
						});
					else if(!(this[keys[i]] instanceof Function))
						mymap.removeLayer(this[keys[i]]);

					break;
				default:

					throw "Unsupported do(action, map) action: '" + action + "'";
					return false; break;
			}

		}

		return true;
	},

};

class LeafletInterface {

	/**
	 * LeafletInterface class
	 *
	 * Is used by the WebsocketHandler class to interact with the LeafletJS map.
	 */

	/**
	 * markersDo(String action, [Variable map])
	 * Primarily, the action "remove" will be used. "clear" is not expected to
	 * be implemented in any use case.
	 *
	 * @param	action	a string that contains either "clear", "addTo", or
	 *					"remove".
	 * @param	map 	optional variable that is only required if action is
	 *					"addTo", as it is required to add markers to the
	 *					specificed target viewer.
	 * @returns			true, always.
	 */
	static markersDo(action, map) {

		var keys = Object.keys(leafletData);

		for(var i = 0; i < keys.length; i++) {

			switch(action) {
				case "clear":

					if(leafletData[keys[i]] instanceof Array)
						leafletData[keys[i]].length = 0;
					else if(!leafletData[keys[i]] instanceof Function)
						leafletData[keys[i]] = null;

					break;
				case "addTo":

					if(leafletData[keys[i]] == null || leafletData[keys[i]] == [])
						break;

					if(leafletData[keys[i]] instanceof Array)
						leafletData[keys[i]].forEach(function(element) {
							element.addTo(map);
						});
					else if(!leafletData[keys[i]] instanceof Function)
						leafletData[keys[i]].addTo(map);

					break;
				case "remove":

					if(leafletData[keys[i]] == null || leafletData[keys[i]] == [])
						break;

					if(leafletData[keys[i]] instanceof Array)
						leafletData[keys[i]].forEach(function(element) {
							mymap.removeLayer(element);
						});
					else if(!leafletData[keys[i]] instanceof Function)
						mymap.removeLayer(leafletData[keys[i]]);

					break;
				default:

					throw "Unsupported markersDo(action) action: '" + action + "'";

					break;
			}

		}

		if(action == "remove")
			LeafletInterface.markersDo("clear");

		return true;

	}

}

// WebsocketHandler & WebsocketController Variables
var websocket = null;
var websocketEndpointURL = "";
var websocketRequestNum = 0;

class WebsocketHandler {

	/**
	 * Handles the connection to the websocket.
	 *
	 * Is used by class WebsocketControls.
	 */

	/**
	 * init()
	 *
	 * Initializes a connection to the websocket. If the connection is successful
	 */
	static init() {

		websocketEndpointURL = "ws://" + $("#url").val() + ":8000/";
		websocket = new WebSocket(websocketEndpointURL);

		websocket.onopen = function(evt) {

			// when a connection with the websocket is initially established
			console.log("OK: Websocket connection with " + websocketEndpointURL +
				" is successful.");

			if(websocket.readyState === websocket.OPEN) {

				WebsocketHandler.update();

				console.log("APPROVED WEBSOCKET CONNECTION OPEN: " +
					websocket.readyState);

				return true;

			} else {

				console.log("Websocket connection failed, unknown error.");
				console.log(websocket.readyState);

				return false;

			};

		};

		websocket.onmessage = function(evt) {

			// when this script receives a message from the websocket

			// get topical response data
				var data = JSON.parse(evt.data);

				var flightData = [ "alt", "dir", "speed", "velocity" ];

				for(var i = 0; i < flightData.length; i++)
					if(flightData[i] == "dir")
						$("#" + flightData[i]).html((data[flightData[i]]).toFixed(2) + "&deg;");
					else
						$("#" + flightData[i]).html((data[flightData[i]]).toFixed(2));

				// drone pos
				console.log("DRONE POSITION LAT: " + data["lat"] + " LONG: " + data["long"]);

				if(leafletData.waypoints_points.length == 0) {
					console.log("Setting up markers...");
				} else {
					console.log("Updating markers...");
					leafletData.do("remove", mymap);
				}

				leafletData.drone_pos_point =
					L.circle(
						[data["lat"], data["long"]],
						{radius: 1, color: "blue", title: "DRONE"}
					);

				console.log(leafletData.drone_pos_point);

			// get data package from websocket
			var data = data["0"];

			// MARKERS AND LINE: mission waypoints
			var result = DataConverters.line(
				data["mission_waypoints"],
				"yellow",
				true,
				"Waypoints",
				Icon_markerYellow
			);

			leafletData.waypoints_line = result[0];
			leafletData.waypoints_points = result.slice(1);

			// MARKERS AND LINE: searchgrid
			var result = DataConverters.line(
				data["search_grid_points"],
				"green",
				true,
				"Search Point",
				Icon_searchPoint
			);

			leafletData.search_grid_line = result[0];
			//leafletData.search_grid_points = result.slice(1);
			//^turning this from line into polygon

			// LINE: fly zone
			leafletData.fly_zone_line = DataConverters.line(
				data["fly_zones"][0]["boundary_pts"].concat(
					data["fly_zones"][0]["boundary_pts"][0]),
					"red",
					false,
					"",
					""
			);

			// air drop pos
			leafletData.air_drop_pos_point =
				DataConverters.marker(
					data["air_drop_pos"], "Air Drop Position", Icon_markerRed
				);
			// emergent last known pos
			leafletData.emergent_last_know_pos_point =
				DataConverters.marker(
					data["emergent_last_known_pos"], "Emergent Target Last Known Position", Icon_markerBlue
				);
			// air drop pos
			leafletData.home_pos_point =
				DataConverters.marker(data["home_pos"], "Home", Icon_markerGreen);
			// air drop pos
			leafletData.off_axis_target_pos_point =
				DataConverters.marker(
					data["off_axis_target_pos"], "Off Axis Target Position", Icon_markerRed
				);

			/*obstacles_circles: [],*/

			// obstacles
				// stationary obstacles
				leafletData.obstacles_circles =
					DataConverters.circle(
						data["stationary_obstacles"], false, -1, "red", "Stationary Obstacle"
					);
				// moving obstacles
				leafletData.obstacles_circles = leafletData.obstacles_circles.concat(
					DataConverters.circle(
						data["moving_obstacles"], false, -1, "orange", "Moving Obstacle")
					);

			//LeafletInterface.markersDo("addTo", mymap);
			leafletData.do("addTo", mymap);

		};

		websocket.onclose = function(evt) {

			//LeafletInterface.markersDo("remove", mymap);
			leafletData.do("remove", mymap);

		};

		websocket.onerror = function(evt) {

			console.log("ERROR: Failed to connect to websocket. See details:");
			console.log(evt);

			websocket = null;
			websocketEndpointURL = "";
			websocketRequestNum = 0;

		};

	}

	/**
	 * update()
	 *
	 * This is a looping function that continously sends the String "update" to
	 * the websocket in order to provoke a response from the websocket server.
	 */
	static update() {

		var updates = setInterval(function() {

			if(websocketEndpointURL != "" && websocket.readyState == websocket.OPEN) {

				// where the updates are requested
				console.log("Requested update #" + (websocketRequestNum++) +
					" : " + websocket.send("update"));

			} else {

				console.log("INFO: Disconnected from websocket.");
				alert("ALERT: Disconnected from websocket.");

				clearInterval(updates);

				// TODO: fix this, it only removes a quarter of markers and lines
				leafletData.do("remove", mymap);

			}

		}, 500);

	}

	/**
	 * close()
	 *
	 * Closes the connection with the websocket.
	 *
	 * @returns		true if successful, false if not.
	 */
	static close() {

		if(websocketEndpointURL != "") {

			if(websocket.readyState === websocket.OPEN) websocket.close();

			websocket = null;
			websocketEndpointURL = "";
			websocketRequestNum = 0;

			return true;

		} else {

			console.log("ERROR: Attempted to close a websocket connection that's not open.");

			return false;

		}

	}

}

class WebsocketControls {

	/**
	 * WebsocketControls class
	 *
	 * Contains all the functions that are triggered by the UI to launch a
	 * connection to the websocket.
	 */

	/**
	 * doConnect()
	 *
	 * Launches a connection to the websocket.
	 */
	static doConnect() {

		if(websocket == null) {

			websocket = new WebsocketHandler();

			WebsocketHandler.init();

			// TODO add alert for failure to connect
			alert("OK: Successfully connected to the websocket.");

		} else {

			alert("ERROR: A connection to the websocket already exists.");

		};

	};

	/**
	 * doDisconnect()
	 *
	 * Disconnects from the websocket, if a connection is active.
	 *
	 * @returns		nothing.
	 */
	static doDisconnect() {

		console.log("WebsocketControls: Disconnecting from websocket...");

		if(websocketEndpointURL != "") {

			websocket.close();

			websocket = null;
			websocketEndpointURL = "";
			websocketRequestNum = 0;

		} else {

			alert("You are not connected to the websocket.");

		}


	};

	/**
	 * doPause()
	 *
	 * Stops the updates from the server.
	 *
	 * @returns		nothing.
	 */
	static doPause() {

		let alertMessage = "This functionality has not been implemented yet.";

		alert(alertMessage);
		console.log(alertMessage);

	};

}

// icons
iS = [32, 32]; iA = [iS[0]/2, iS[1]]; pA = [0, iS[0]];

// TODO: Add retina version of markers
var Icon_drone = L.icon({
	iconUrl: 'rsc/img/icons/128-map-drone-green.png',
	iconSize: iS,
	iconAnchor: iA,
	popupAnchor: pA
});

var Icon_markerRed = L.icon({
	iconUrl: 'rsc/img/icons/128-map-marker-red.png',
	iconSize: iS,
	iconAnchor: iA,
	popupAnchor: pA
});

var Icon_markerBlue = L.icon({
	iconUrl: 'rsc/img/icons/128-map-marker-blue.png',
	iconSize: iS,
	iconAnchor: iA,
	popupAnchor: pA
});

var Icon_markerGreen = L.icon({
	iconUrl: 'rsc/img/icons/128-map-marker-green.png',
	iconSize: iS,
	iconAnchor: iA,
	popupAnchor: pA
});

var Icon_markerPurple = L.icon({
	iconUrl: 'rsc/img/icons/128-map-marker-purple.png',
	iconSize: iS,
	iconAnchor: iA,
	popupAnchor: pA
});

var Icon_markerYellow = L.icon({
	iconUrl: 'rsc/img/icons/128-map-marker-yellow.png',
	iconSize: iS,
	iconAnchor: iA,
	popupAnchor: pA
});

var Icon_searchPoint = L.icon({
	iconUrl: 'rsc/img/icons/128-map-search-green.png',
	iconSize: iS,
	iconAnchor: [iS[0]/2, iS[1]/2],
	popupAnchor: [0, 32]
});

// end of script

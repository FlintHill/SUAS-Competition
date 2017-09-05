// essential functions
function screwMeUp() {
	$.when($.when($.when($.when($.when().then()).then()).then()).then()).then(console.log("shamrock shakes"));
	return null;
};
function sleep(milliseconds) {
	var start = new Date().getTime();
	for (var i = 0; i < 1e7; i++) {
		if ((new Date().getTime() - start) > milliseconds){
			break;
		}
	}
};

// websocket markers
var waypoints = [], waypoints_line = null, waypoints_latlngs = [], search_grid_points = [], search_grid_line = null, search_grid_latlngs = [];

var fly_zone_line = null, fly_zone_latlngs = [];

var air_drop_pos_point = null, emergent_last_know_pos_point = null, home_pos_point = null, off_axis_target_pos_point = null;

function markersDo(action) {
	console.log("markersDo('" + action + "')");

	switch(action) {
		case "clear":
			// clears variables
			waypoints.length = 0;
			waypoints_latlngs.length = 0;
			waypoint_line = null;

			search_grid_points.length = 0;
			search_grid_latlngs.length = 0;
			search_grid_line.length = 0;

			fly_zone_line = null;
			fly_zone_latlngs.length = 0;
			break;
		case "addTo":
			waypoints.forEach(function(element) {
				element.addTo(mymap);
			});
			search_grid_points.forEach(function(element) {
				element.addTo(mymap);
			})

			air_drop_pos_point.addTo(mymap);
			emergent_last_known_pos_point.addTo(mymap);
			home_pos_point.addTo(mymap);
			off_axis_target_pos_point.addTo(mymap);
			break;
		case "remove":
			// removes from leaflet map
			if(waypoints.length !== 0) {
				waypoints.forEach(function(element) { element.remove(); });
				waypoints_line.remove();

				search_grid_points.forEach(function(element) { element.remove(); })
				search_grid_line.remove();

				fly_zone_line.remove();

				air_drop_pos_point.remove();
				emergent_last_known_pos_point.remove();
				home_pos_point.remove();
				off_axis_target_pos_point.remove();

				markersDo('clear');
			} else {
				console.log("Not clearing all points and lines because they're already empty");
			}
			break;
		default:
			throw "Unsupported markersDo(action) action: '" + action + "'";
	}

	return true;
}

// websocket
var websocketEndpointURL = "";
var websocket = null;

function doConnect() {
	websocketEndpointURL = "ws://" + $("#url").val() + ":8000/";

	console.log("Launching websocket connection to '" + websocketEndpointURL + "'")
	websocket = new WebSocket(websocketEndpointURL);

	/*
	websocket.onopen = function(evt) { onOpen(evt) };
	websocket.onmessage = function(evt) { console.log("ONMESSAGE"); console.log(evt); onMessage(evt) };
	websocket.onclose = function(evt) { onClose(evt) };
	*/

	websocket.onopen = function(evt) {
		console.log("Connected to websocket.");

		var updates = setInterval(function(){
			if(websocketEndpointURL != "") {
				console.log("Requested update " + websocket.send("update"));
			} else {
				alert("Disconnected from websocket")
				clearInterval(updates);
			}
			//websocket.send("update");
			// add in disconnect functionality
			// http://stackoverflow.com/questions/16437173/stop-setinterval
		}, 3000);
	};
	websocket.onmessage = function(evt) {
		console.log("EVENT DATA");
		console.log(evt);

		// update positions of obstacles
		var d = evt.data;

		if(JSON.parse(d).obstacle_present == true)
			$("#warning").removeClass("hidden");
		else
			$("#warning").addClass("hidden");

		$("#alt").html((JSON.parse(d).alt).toFixed(2));
		$("#dir").html((JSON.parse(d).dir).toFixed(2));
		$("#speed").html((JSON.parse(d).speed).toFixed(2));
		$("#velocity").html((JSON.parse(d).velocity).toFixed(2));

		/* draw on map: 
		 * - drone.....................// 
		 * - fly_zone..................// red border, no fill
		 * - air_drop_pos..............// marker, red
		 * - emergent_last_known_pos...// marker, blue
		 * - home_pos..................// marker, green
		 * - off_axis_target_pos.......// marker, purple
		 * - mission_waypoints.........// markers, yellow. all markers connected with solid yellow line.
		 * - search_grid_points........// markers, green. all " connected with 'stroke dash pattern' green line.
		 *
		 * needs a seperate request for obstacles
		 */

		var data = JSON.parse(evt.data)["0"];

		if(waypoints.length == 0) {
			console.log("Setting up markers...");
			///////// setup

			// mission_waypoints.........// markers, yellow. all markers connected with solid yellow line
			// search_grid_points........// markers, green. all " connected with 'stroke dash pattern' green line
			waypoints_latlngs = [];
			search_grid_latlngs = [];
			fly_zone_latlngs = [];

			for(var i = 0; i < data["mission_waypoints"].length; i++) {
				// MISSION WAYPOINTS
				var mission_location = [data["mission_waypoints"][i].latitude, data["mission_waypoints"][i].longitude];

				waypoints[i] = L.marker(mission_location, {icon: Icon_markerYellow, title: 'Waypoint #' + data["mission_waypoints"][i].order});

				waypoints_latlngs.push(mission_location);
			}

			for(var i = 0; i < data["search_grid_points"].length; i++) {
				// SEARCH GRID POINTS
				var search_grid_location = [data["search_grid_points"][i].latitude, data["search_grid_points"][i].longitude];

				search_grid_points[i] = L.marker(search_grid_location, {icon: Icon_searchPoint, title: 'Search Point #' + data["search_grid_points"][i].order});
				search_grid_latlngs.push(search_grid_location);
			}

			for(var i = 0; i < data["fly_zones"][0]["boundary_pts"].length; i++ ) {
				var fly_zone_location = [data["fly_zones"][0]["boundary_pts"][i].latitude, data["fly_zones"][0]["boundary_pts"][i].longitude];

				fly_zone_latlngs.push(fly_zone_location);
			}
			fly_zone_latlngs.push([data["fly_zones"][0]["boundary_pts"][0].latitude, data["fly_zones"][0]["boundary_pts"][0].longitude]);

			waypoints_line = L.polyline(waypoints_latlngs, {color: 'yellow', interactive: false}).addTo(mymap);
			search_grid_line = L.polyline(search_grid_latlngs, {color: 'green', interactive: false}).addTo(mymap);
			fly_zone_line = L.polyline(fly_zone_latlngs, {color: 'red', weight: 9, opacity: 0.8, interactive: false}).addTo(mymap);

			// var air_drop_pos_point = null, emergent_last_know_pos_point = null, home_pos_point = null, off_axis_target_pos_point = null;

			air_drop_pos_point = L.marker(
				[
					data["air_drop_pos"].latitude, 
					data["air_drop_pos"].longitude
				], 
				{icon: Icon_markerRed, title: 'Air Drop Position'}
			);

			emergent_last_known_pos_point = L.marker(
				[
					data["emergent_last_known_pos"].latitude, 
					data["emergent_last_known_pos"].longitude
				], 
				{icon: Icon_markerBlue, title: 'Emergent Target Last Known Position'}
			);

			home_pos_point = L.marker(
				[
					data["home_pos"].latitude, 
					data["home_pos"].longitude
				], 
				{icon: Icon_markerGreen, title: 'Home'}
			);

			off_axis_target_pos_point = L.marker(
				[
					data["off_axis_target_pos"].latitude, 
					data["off_axis_target_pos"].longitude
				], 
				{icon: Icon_markerPurple, title: 'Off Axis Target Position'}
			);

			markersDo("addTo");
		} else {
			console.log("Updating markers...");
			///////// update

			// mission_waypoints.........// markers, yellow. all markers connected with solid yellow line
			// search_grid_points........// markers, green. all " connected with 'stroke dash pattern' green line
			waypoints_latlngs = [];
			search_grid_latlngs = [];
			fly_zone_latlngs = [];

			for(var i = 0; i < data["mission_waypoints"].length; i++) {
				// MISSION WAYPOINTS
				var mission_location = [data["mission_waypoints"][i].latitude, data["mission_waypoints"][i].longitude];

				if(typeof waypoints[i] !== 'undefined') 
					waypoints[i].setLatLng(mission_location);
				else if(waypoints[i] === null)
					waypoints[i].remove();
				else
					waypoints[i] = L.marker(mission_location, {icon: Icon_markerYellow, title: 'Waypoint #' + data["mission_waypoints"][i].order});
				
				waypoints_latlngs.push(mission_location);
			}

			for(var i = 0; i < data["search_grid_points"].length; i++) {
				var search_grid_location = [data["search_grid_points"][i].latitude, data["search_grid_points"][i].longitude];

				if(typeof search_grid_points[i] !== 'undefined')
					search_grid_points[i].setLatLng(search_grid_location);
				else if(search_grid_points[i] === null)
					search_grid_points[i].remove();
				else
					search_grid_points[i] = L.marker(mission_location, {icon: Icon_searchPoint, title: 'Search Point #' + data["mission_waypoints"][i].order});

				search_grid_latlngs.push(search_grid_location);
			}

			for(var i = 0; i < data["fly_zones"][0]["boundary_pts"].length; i++ ) {
				var fly_zone_location = [data["fly_zones"][0]["boundary_pts"][i].latitude, data["fly_zones"][0]["boundary_pts"][i].longitude];

				fly_zone_latlngs.push(fly_zone_location);
			}
			fly_zone_latlngs.push([data["fly_zones"][0]["boundary_pts"][0].latitude, data["fly_zones"][0]["boundary_pts"][0].longitude]);

			waypoints_line.remove();
			search_grid_line.remove();
			fly_zone_line.remove();

			waypoints_line = L.polyline(waypoints_latlngs, {color: 'yellow', interactive: false}).addTo(mymap);
			search_grid_line = L.polyline(search_grid_latlngs, {color: 'green', interactive: false}).addTo(mymap);
			fly_zone_line = L.polyline(fly_zone_latlngs, {color: 'red', weight: 4.5, opacity: 0.8, interactive: false}).addTo(mymap);

			//marks instanceof L.Marker
		}

		sleep(1000); websocket.send("update");
	}
	websocket.onclose = function(evt) {
		console.log("Disconnected from websocket.");
		websocketEndpointURL = "";
	}
};

function doDisconnect() {
	if(websocketEndpointURL != "")
		websocketEndpointURL = "";
	else
		alert("You are not connected to the websocket.").

	console.log("WebSocket DISCONNECT");
	websocket.close();
};
function doPause() {
	console.log("This functionality has not been implemented yet.");
};

// interface
function rips() {
	if( $("#information").css("display") == "block" ) {
		$("#information").css("display", "none");
		$("#dropdown").text("Show Description"); // &uarr;
	} else {
		$("#information").css("display", "block");
		$("#dropdown").text("Show Description"); // &darr;
	}
};

/*
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
		'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="http://mapbox.com">Mapbox</a>',
	id: 'mapbox.streets'
}).addTo(mymap);
*/

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
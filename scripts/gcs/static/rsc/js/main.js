/**
 * main script file for gcs:web ui
 *
 * @author		James Villemarette
 * @version 	0.1
 * @since		2017-10-23
 */

// page init

$(document).ready(function(){

	// materialize ui starts
	$('ul.tabs').tabs();
	$('select').material_select();
	$('.tooltipped').tooltip();

	$('.modal').modal();

	$("#size-lock-button").hover(function() {
		// hover enter
		if(!$("#size-lock-icon").hasClass("fa-unlock"))
			$("#size-lock-icon").removeClass("fa-lock").addClass("fa-unlock-alt");
	}, function() {

		// hover leave
		if(!$("#size-lock-icon").hasClass("fa-unlock"))
			$("#size-lock-icon").removeClass("fa-unlock-alt").addClass("fa-lock");

	});

	// lockdown mts interface
	MTSFields.forEach(function(element) {
		$("[value='" + element + "']").attr("disabled", "");
	});

	$("#target-content").attr("disabled", "")

});

// key combo watchdog

$(document).keydown(function(event) {

	if(event.ctrlKey == true) {
		console.log("keydownWatchdog: Control keyed.");

		// all key bindings use control key, first

		switch(event.keyCode) {
			case 38: // up arrow
				loadImages();
				break;
			case 37: // left arrow
				if(!$("a[name='left-button']").hasClass("disabled"))
					imageSelect('left');
				break;
			case 39: // right arrow
				if(!$("a[name='right-button']").hasClass("disabled"))
					imageSelect('right');
				break;
			case 13: // enter
				$('#verification').modal('open');
				break;
		}
	};

});

// image height and width adjust

var imageHeightLocked = true, establishedLockHeight = 0;

$(document).ready(function() {

	establishedLockHeight = $("#image-previewer-parent-container").height();

});

/**
 * switchImageHeightLock()
 *
 * Toggles all the relevant elements to whether or not the image's
 * height should be locked to the height of the viewer box that it
 * is.
 *
 * If it is locked, the image will be as tall as possible, and
 * thereby as wide (within the aspect ratio) as it can be within the
 * viewer box.
 *
 * IF it is NOT locked, the image will only be as wide as possible,
 * and there by as tall (within the aspect ratio) as it can be
 * within the viewer box.
 *
 * returns nothing.
 */
function switchImageHeightLock() {

	if(imageHeightLocked) {
		$("#image-previewer").removeAttr("height");
		$("#image-previewer").attr("width", $("#image-previewer-container").width() + "px");

		imageHeightLocked = false;
		$("#size-lock-icon").removeClass("fa-lock fa-unlock-alt").addClass("fa-unlock");
		$("#size-lock-button").addClass("shift-lock-icon");
	} else {
		$("#image-previewer").removeAttr("width");
		$("#image-previewer").attr("height", establishedLockHeight + "px");

		imageHeightLocked = true;
		$("#size-lock-icon").removeClass("fa-unlock").addClass("fa-lock");
		$("#size-lock-button").removeClass("shift-lock-icon");
	}

}

var currentImage = 0, totalImages = 0, zoomLevel = 1;

/**
 * updateCounters()
 *
 * Reflect the counters directly above this function onto the web 
 * page.
 */
function updateCounters() {

	$("#current-image").html(currentImage + 1);
	$("#total-images").html(totalImages);
	$("#zoom-level").html(zoomLevel);

}

/**
 * indexExistsIn(array arr, int i)
 *
 * arr is an array [] containing at least one element.
 * i is index.
 *
 * returns true if an index, i, exists within array, arr.
 */
function indexExistsIn(arr, i) {

	if(i < arr.length && i >= 0)
		return true;

}

/**
 * showImage(int index)
 *
 * Put up an image in the viewer from imgs array at specific index.
 *
 * throws error if index below or beyond array elements.
 *
 * returns nothing.
 */
function showImage(index) {

	if(!indexExistsIn(imgs, index))
		throw "showImage(index): Index out of bounds error: " + index + ".";

	currentImage = index;

	$("#image-previewer").attr("src", "get/imgs/" + imgs[index]);
	$("#current-image").html(currentImage);

	updateCounters();

}

/**
 * imageSelect(string direction)
 *
 * Moves "left" or "right" (direction) by one image.
 *		  ^			^
 */
function imageSelect(direction) {

	var change = 0;

	if(direction == "left")
		change = -1;
	else if(direction == "right")
		change = 1;
	else
		throw "imageSelect(direction): Unknown cardinal horizontal direction '" + direction + "'";

	if(indexExistsIn(imgs, currentImage + change))
		showImage(currentImage + change);

	updateDirectionalButtons();

}

/**
 * updateDirectionalButtons()
 *
 * Updates the directional buttons for switching between images
 * appropriately.
 */
function updateDirectionalButtons() {

	// left button
	if(currentImage == 0)
		$("a[name='left-button']").addClass('disabled');
	else
		$("a[name='left-button']").removeClass('disabled');

	// right button
	if(currentImage == (totalImages - 1))
		$("a[name='right-button']").addClass('disabled');
	else
		$("a[name='right-button']").removeClass('disabled');

}

var cropData = {

	targetTopLeftX: 0,
	targetTopLeftY: 0,

	targetBottomRightX: 0,
	targetBottomRightY: 0,

	imageFilename: "",

};

/**
 * loadCropPreview()
 *
 * Triggered by the "Crop and Submit" button.
 *
 * Adds CSS stylings to a #image-preview div box that displays a rough preview
 * of the crop that was selected in MTS.
 */
function loadCropPreview() {

	// display crop preview
	$(document).ready(function() {

		// TODO: concatenate code.

		var imageW = $('#image-previewer')[0].naturalWidth; 
		var imageH = $('#image-previewer')[0].naturalHeight;

		var cropperW = $("#image-previewer").width();
		var cropperH = $("#image-previewer").height();

		var length = Math.round($("#crop-detail-panel").height());
		var topLeftX = selectionPoints[0][0];
		var topLeftY = selectionPoints[0][1];
		var extrude = selectionPoints[1][0] - selectionPoints[0][0];

		var transformedW = ((length/extrude) * imageW)/(imageW/cropperW);
		var transformedH = ((length/extrude) * imageH)/(imageH/cropperH);

		var actual_topLeftX = (topLeftX/cropperW) * imageW;
		var actual_topLeftY = (topLeftY/cropperH) * imageH;

		var transformed_topLeftX = (transformedW/imageW) * actual_topLeftX;
		var transformed_topLeftY = (transformedH/imageH) * actual_topLeftY;

		// TODO: delete when crop preview solved
		console.log("imageW: " + imageW);
		console.log("imageH: " + imageH);
		console.log("cropperW: " + cropperW);
		console.log("cropperH: " + cropperH);
		console.log("length: " + length);
		console.log("topLeftX: " + topLeftX);
		console.log("topLeftY: " + topLeftY);
		console.log("extrude: " + extrude);
		console.log("transformedW: " + transformedW);
		console.log("transformedH: " + transformedH);
		console.log("actual_topLeftX: " + actual_topLeftX);
		console.log("actual_topLeftY: " + actual_topLeftY);
		console.log("transformed_topLeftX: " + transformed_topLeftX);
		console.log("transformed_topLeftY: " + transformed_topLeftY);

		$("#crop-previewer").css({
			"height": length + "px", 
			"width": length + "px",

			"border": "1px solid black",

			"background-image": "url('imgs/" + imgs[currentImage] + "')",
			"background-repeat": "no-repeat",
			"background-attachment": "scroll", // fixed

			// TODO: crop preview relation
			"background-size": transformedW + "px " + transformedH + "px",
			"background-position": 
				"-" + 
				(transformed_topLeftX + (50)) + // 17
				"px -" + 
				(transformed_topLeftY + (34)) + // 17
				"px"
		});

		console.log("loadCropPreview(): imageW: " + imageW);
		console.log("loadCropPreview(): length: " + length);
		console.log("loadCropPreview(): extrude: " + extrude);

		// store
		var actual_extrude = (extrude/cropperW) * imageW;

		cropData.targetTopLeftX = Math.round(actual_topLeftX);
		cropData.targetTopLeftY = Math.round(actual_topLeftY);
		cropData.targetBottomRightX = Math.round(actual_topLeftX + actual_extrude);
		cropData.targetBottomRightY = Math.round(actual_topLeftY + actual_extrude);

		cropData.imageFilename = imgs[currentImage];

		// load table data
		$("#preview-filename").html(imgs[currentImage]);
		$("#preview-x1").html(Math.round(actual_topLeftX));
		$("#preview-y1").html(Math.round(actual_topLeftY));
		$("#preview-x2").html(Math.round(actual_topLeftX + actual_extrude));
		$("#preview-y2").html(Math.round(actual_topLeftY + actual_extrude));
		$("#preview-extrusion").html(Math.round(actual_extrude));

	});

}

/**
 * submitTarget()
 *
 * Triggered by Crop Image Previewer modal in MTS.
 *
 * Posts an AJAX request to back-end flask script the details of the crop, not
 * the actual crop itself. This also pushes the crop data (shape, color, etc.)
 *
 * returns nothing.
 */
function submitTarget() {

	$.ajax({
		url: "/post/target",
		method: "POST",
		timeout: 1000,

		data: {
			targetTopLeftX: cropData.targetTopLeftX,
			targetTopLeftY: cropData.targetTopLeftY,

			targetBottomRightX: cropData.targetBottomRightX,
			targetBottomRightY: cropData.targetBottomRightY,

			imageFilename: cropData.imageFilename,

			targetShape: $("#target-shape").val(),
			targetColor: $("#target-color").val(),
			targetContent: $("#target-content").val(),
			contentColor: $("#content-color").val(),
			targetOrientation: $("#target-orientation").val()
		},

		dataType: "json",

		success: function(data) {
			// interop was enabled
			Materialize.toast("SUCCESS: Sent target to backend script.");

			console.log("submitTarget(): ajax data:")
			console.log(data);

			updateCounters();
		},

		error: function(data) {
			// server side error
			Materialize.toast("FAILURE: Unable to send target; See console.");

			console.log("submitTarget(): ajax data:");
			console.log(data);
		}
	});

}

// control panel code

var refresh = null;

/**
 * switchControlPanelRefresh()
 *
 * Enable or disable the automatic control panel refresh.
 *
 * returns nothing.
 */
function switchControlPanelRefresh() {

	if($("#switch-control-panel-icon").hasClass("fa-spin")) {
		// stop auto refreshing
		$("#switch-control-panel-icon").removeClass("fa-spin");

		clearInterval(refresh);
	} else {
		// start auto refreshing
		$("#switch-control-panel-icon").addClass("fa-spin");

		refresh = setInterval(function() { statusGet(); }, 1000); // 1000ms = 1s
	}

}

// front-to-backend code

/**
 * statusDisplay(String programName, String status)
 *
 * Front-end update function that's used by statusPush() and statusGet().
 *
 * Updates the Control Panel slide with the data that was received by the back-
 * end script.
 *
 * returns nothing.
 */
function statusDisplay(programName, data) {

	var ref = "#" + programName;

	$(ref + "-status").html(data["status"]);

	if(programName == "interop" && data["request_status"] != "failure") {
		var interopProperties = ["emergent_position", "airdrop_position", "off-axis_position"];

		interopProperties.forEach(function(element) {
			$(ref + "-" + element).html("[" + data[element][0] + ", " + data[element][1] + "]");
		});
	} else {
		$(ref + "-runtime").html(data["runtime"]);
	}

	if(data["status"] == "connected") { // connected

		if(!$(ref + "-light").hasClass("green")) {
			$(ref + "-light").removeClass("red").addClass("green");
			$(ref + "-light-text").html("Connected");

			console.log("HELP1 " + ref + "-power-button");

			$(ref + "-power-button").removeClass("green").addClass("red");
			$(ref + "-power-button").attr("onclick", "statusPush('" + programName + "', 'off');");
		}

	} else if(data["status"] == "disconnected") { // disconnected

		if(!$(ref + "-light").hasClass("red")) {
			$(ref + "-light").removeClass("green").addClass("red");
			$(ref + "-light-text").html("Disconnected");

			console.log("HELP2 " + ref + "-power-button");

			$(ref + "-power-button").removeClass("red").addClass("green");
			//$(ref + "-power-button").attr("data-tooltip", "Turn on");
			$(ref + "-power-button").attr("onclick", "statusPush('" + programName + "', 'on');");
		}

	}

}

/**
 * statusPush(String process, String cmd)
 *
 * Turn on or off a subprocess, with the subprocessesing being:
 *	- "interop-connection",
 *	- "sda", and
 *	- "image-processing"
 * by posting an AJAX request to the back-end script.
 *
 * returns nothing.
 */
function statusPush(process, cmd) {

	toastDuration = 4000;

	// precondition: cmd valid
	if(cmd != "off" && cmd != "on")
		throw "statusChange(process, cmd ): Unknown String cmd '" + process + "'";

	var program = "", friendlyProgramName = "";
	
	switch(process) {
		case "sda":
			program = "sda";
			friendlyProgramName = "SDA script";
			break;
		case "img_proc":
			program = "img_proc";
			friendlyProgramName = "Image Processing script"
			break;
		default:
			// precondition: process requested valid
			throw "statusChange(process, cmd): Unknown String process '" + process + "'";
	}

	var urlCommand = "", shortCommand = "", command = "";

	if(cmd == "off") {
		// turn off
		urlCommand = "disconnected";
		shortCommand = "stop";
		command = "stopped"
	} else {
		// turn on
		urlCommand = "connected";
		shortCommand = "start";
		command = "started";
	}

	Materialize.toast('Sent ' + shortCommand.toUpperCase() + ' command to Interop. script.', toastDuration);

	$.ajax({
		url: "/post/" + program + "/" + urlCommand,
		method: "POST",
		timeout: 1000,

		dataType: "json",

		success: function(data) {
			// interop was enabled
			Materialize.toast(friendlyProgramName + ' was ' + command.toUpperCase() + '.', toastDuration);
			console.log("statusPush():" + friendlyProgramName + ' successfully ' + command + ', see data: ');
			console.log(data);

			statusDisplay(program, data);

			statusGet(program);
		},

		error: function(data) {
			// server side error
			Materialize.toast('Failed to ' + shortCommand + ' ' + friendlyProgramName + '; See console.', toastDuration);
			console.log("statusPush(): " + friendlyProgramName + ' failed to be ' + command + ', see data: ');
			console.log(data);
		}
	});

}

/**
 * statusGet()
 *
 * Retrieves the status informaition of the different subprocesses for the 
 * control panel.
 *
 * returns nothing.
 */
function statusGet(programName) {

	if(typeof programName == "undefined") {

		const programs = ["interop", "img_proc", "sda"];

		programs.forEach(function(program) {
			statusGet(program);
		});

		return;

	}

	$.ajax({
		url: "/get/" + programName,
		method: "POST",
		timeout: 1000,
		async: true,

		dataType: "json",

		success: function(data) {
			statusDisplay(programName, data);
		},

		error: function(data) {
			// server side error
			Materialize.toast('See console: /get/' +  programName + ' failed.', 1000);
			console.log("statusGet(): /get/" + programName + ' failed, see data: ');
			console.log(data);
		}
	});

}

// init code

var imgs = [], ias = null, selectionPoints = [];

/**
 * loadImages()
 *
 * Starter function that loads in all available images by
 * requesting the directory listing from a PHP/whatever script that
 * returns a JSON array of the directories contents (excluding sys
 * files and the script itself) in the following form:
 *
 * 	[
 *		0 => "demo-1.jpg"
 *		1 => "demo-2.jpg"
 *		n => ...
 * 	]
 *
 * throws nothing.
 *
 * returns nothing.
 */
function loadImages() {

	$.ajax({
		url: "get/imgs", // "imgs/get.php"
		
		success:function(data) {
			console.log("loadImages(): Images Loaded:");
			console.log(data);

			// parse available image info
			var length = Object.keys(data).length;
			totalImages = length;

			$("#total-images").html(length);

			for(var i = 0; i < length; i++)
				if($(imgs).index(Object.values(data)[i]) == -1)
					imgs.push(Object.values(data)[i])

			// if no images exist
			if(length == 0) {
				console.log("loadImages(): No images available.");

				$("#current-image").html(0);
				Materialize.toast("LOAD IMAGES SUCESS: No images available.", 3700);
				
				return;
			} else {
				enableMTSButtons();
			}

			if(currentImage != 0)
				if(currentImage < Object.values(data).length) // if image index still exists (b/c images will be deleted)
					showImage(currentImage); // maintain image index
				else
					showImage(0); // presumed always present
			else
				showImage(0);

			// initialize image area selector
			ias = $('#image-previewer').imgAreaSelect({ 
				aspectRatio: '1:1', 
				handles: true,

				onSelectEnd: function (img, selection) {
					$("a[name='remove-crop-button']").removeClass("disabled");
					$("a[name='crop-and-submit-button']").removeClass("disabled");

					var s = selection;

					selectionPoints = [
						[s.x1, s.y1],
						[s.x2, s.y2]
					];
				}
			});

			$("#image-previewer").attr("height", $("#image-previewer-parent-container").height() + "px"); // this has to be second b/c imgAreaSelect resets the height attribute.

			updateDirectionalButtons();

			// indicate
			Materialize.toast('Images successfully loaded.', 2400);
		},

		error:function(data) {
			// indicate
			Materialize.toast('Failed to load images, check console.', 4000);

			console.log("loadImages(): Unknown connection error, see:");
			console.log(data);
		}
	});

}

const MTSFields = ["Shape", "Shape Color", "Alphanumeric Color", "Orientation"];

/**
 * enableMTSButtons()
 *
 * Only executes once. Opens up MTS screen buttons and fields.
 *
 * returns nothing.
 */
function enableMTSButtons() {

	$("#size-lock-button").removeClass("disabled");

	MTSFields.forEach(function(element) {
		$("[value='" + element + "']").removeAttr("disabled");
	});

	$("#target-content").removeAttr("disabled");

}


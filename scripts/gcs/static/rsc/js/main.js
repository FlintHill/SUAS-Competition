/**
 * main script file
 * v0.1
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

});

// key combo watchdog

$(document).keydown(function(event) {

	if(event.ctrlKey == true) {
		console.log("control keyed ");
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

var currentImage = 0, totalImages = 0, submittedImages = 0;

/**
 * updateCounters()
 *
 * Reflect the counters directly above this function onto the web 
 * page.
 */
function updateCounters() {

	$("#current-image").html(currentImage + 1);
	$("#total-images").html(totalImages);
	$("#submitted-images").html(submittedImages);

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

	$("#image-previewer").attr("src", "imgs/" + imgs[index]);
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
 */
function loadCropPreview() {

	// display crop preview
	$(document).ready(function() {

		// TODO: concatenate code.

		var imageW = $('#image-previewer')[0].naturalWidth; 
		var imageH = $('#image-previewer')[0].naturalHeight;

		var cropperW = $("#image-previewer").width();
		var cropperH = $("#image-previewer").height();

		var length = $("#crop-detail-panel").height();
		var topLeftX = selectionPoints[0][0];
		var topLeftY = selectionPoints[0][1];
		var extrude = selectionPoints[1][0] - selectionPoints[0][0];

		var transformedW = ((length/extrude) * imageW)/(imageW/cropperW);
		var transformedH = ((length/extrude) * imageH)/(imageH/cropperH);

		var actual_topLeftX = (topLeftX/cropperW) * imageW;
		var actual_topLeftY = (topLeftY/cropperH) * imageH;

		var transformed_topLeftX = (transformedW/imageW) * actual_topLeftX;
		var transformed_topLeftY = (transformedH/imageH) * actual_topLeftY;

		$("#crop-previewer").css({
			//"height": length + "px", 
			//"width": length + "px",

			"border": "1px solid black",

			"background-image": "url('imgs/" + imgs[currentImage] + "')",
			"background-repeat": "no-repeat",
			"background-attachment": "scroll", // fixed

			"background-size": transformedW + "px " + transformedH + "px",
			"background-position": 
				"-" + 
				transformed_topLeftX + 
				"px -" + 
				transformed_topLeftY + 
				"px" // "0px 0px"
		});

		console.log("imageW: " + imageW);
		console.log("length: " + length);
		console.log("extrude: " + extrude);

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
 * TODO: Expand doc when tested in real/artificial environment.
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

			imageFilename: cropData.imageFilename
		},

		dataType: "json",

		success: function(data) {
			// interop was enabled
			Materialize.toast("SUCCESS: Sent target to backend script.");

			console.log(data);

			submittedImages++;
			updateCounters();
		},

		error: function(data) {
			// server side error
			Materialize.toast("FAILURE: Unable to send target; See console.");

			console.log(data);
		}
	});

}

// control panel code

/**
 * switchControlPanelRefresh()
 *
 * Enable or disable the automatic control panel refresh.
 */
function switchControlPanelRefresh() {

	if($("#switch-control-panel-icon").hasClass("fa-spin"))
		$("#switch-control-panel-icon").removeClass("fa-spin");
	else
		$("#switch-control-panel-icon").addClass("fa-spin");

	// TODO: make refresh code actually refresh. write this in real env.

}

// front-to-backend code

/**
 * statusPush(String process, String cmd)
 *
 * Turn on or off a subprocess, either:
 *	- "interop-connection"
 *	- "sda"
 *	- "image-processing"
 *
 * TODO: Expand doc when tested in real/artificial environment.
 */
function statusPush(process, cmd) {

	toastDuration = 4000;

	// precondition: cmd valid
	if(cmd != "off" && cmd != "on")
		throw "statusChange(process, cmd ): Unknown String cmd '" + process + "'";

	var program = "", friendlyProgramName = "";
	
	switch(process) {
		case "interop-connection":
			program = "interop";
			friendlyProgramName = "Interop. script";
			break;
		case "sda":
			program = "sda";
			friendlyProgramName = "SDA script";
			break;
		case "image-processing":
			program = "img_proc";
			friendlyProgramName = "Image Processing script"
			break;
		default:
			// precondiiton: process requested valid
			throw "statusChange(process, cmd): Unknown String process '" + process + "'";
	}

	var urlCommand = "", shortCommand = "", command = "";

	if("off" == cmd) {
		// turn off
		urlCommand = "Disabled";
		shortCommand = "stop";
		command = "stopped"
	} else {
		// turn on
		urlCommand = "Enabled";
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
			console.log(friendlyProgramName + 'successfully ' + command + ', see data: ');
			console.log(data);
		},

		error: function(data) {
			// server side error
			Materialize.toast('Failed to ' + shortCommand + ' ' + friendlyProgramName + '; See console.', toastDuration);
			console.log(friendlyProgramName + ' failed to be ' + command + ', see data: ');
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
		url: "imgs/get.php",
		
		success:function(data) {
			console.log("Images Loaded:");
			console.log(data);

			// parse available image info
			var length = Object.keys(data).length;
			totalImages = length;

			$("#total-images").html(length);

			for(var i = 0; i < length; i++)
				if($(imgs).index(Object.values(data)[i]) == -1)
					imgs.push(Object.values(data)[i])

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

					//console.log("x1: " + selection.x1 + " , y1: " + selection.y1); 

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

			console.log("Unknown connection error, see:");
			console.log(data);
		}
	});

}


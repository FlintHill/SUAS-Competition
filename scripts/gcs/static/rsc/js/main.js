/**
 * main script file for gcs:web ui
 *
 * @author		James Villemarette
 * @version 	1.3
 * @since		2018-04-26
 */

// helper functions

/**
 * capitalizeFirstLetter(String str)
 *
 * Capitalizes the first letter of a string and returns of it.
 *
 * @param	str		String to be fixed.
 *
 * @returns	properly upper-cased string.
 */
function capitalizeFirstLetter(str) {
	return str.toLowerCase().replace(/\b[a-z]/g, function(letter) {
		return letter.toUpperCase();
	});
}

/**
 * calcCrow(double lat1, double lon1, double lat2, double lon2)
 *
 * Calculate the distance between two geographic coordinates; as the
 * crow flies.
 *
 * Source: https://stackoverflow.com/a/18883819
 *
 * @param	lat1	first point's latitude.
 * @param	lon1	first point's longitude.
 * @param	lat2	second point's latitude.
 * @param	lon2	second point's longitude.
 *
 * @returns	distance in kilometers.
 */
function calcCrow(lat1, lon1, lat2, lon2) {
    var R = 6371; // km

    var dLat = toRad(lat2 - lat1);
	var dLon = toRad(lon2 - lon1);
    var lat1 = toRad(lat1);
    var lat2 = toRad(lat2);

    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
		Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c;

    return d;
}

/**
 * toRad(integer/double value)
 *
 * Converts numeric degrees to radians.
 *
 * @param	degrees.
 * @returns	radians.
 */
function toRad(Value) {
    return Value * Math.PI / 180;
}


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
	$("#zoom-out-btn").addClass("disabled");
	$("#zoom-in-btn").addClass("disabled");

	MTSFields.forEach(function(element) {
		$("[value='" + element + "']").attr("disabled", "");
	});

	$("#target-content").attr("disabled", "")

	// set compass direction
	$.ajax({
		url: "/get/offset",
		method: "GET",
		timeout: 3000,

		dataType: "json",

		success: function(data) {
			// interop was enabled
			if(data["request_status"] == "success")
				setCompassDirection(data["offset"]);
			else {
				Materialize.toast("FAILURE: Failed to retrieve camera north offset; See console.");

				console.log("$(document).ready() >> function(): '/get/offset' ajax data:");
				console.log(data);

				return;
			}

			console.log("got offset of " + data["offset"]);
		},

		error: function(data) {
			// server side error
			Materialize.toast("FAILURE: Unable to retrieve camera north offset; See console.");

			console.log("$(document.ready() >> function(): '/get/offset/' ajax data:");
			console.log(data);
		}
	});

	// finished initializing
	$("#loading-bar").addClass("hide");

});

// key combo watchdog

$(document).keydown(function(event) {

	if(event.shiftKey) {
		console.log("keydownWatchdog: Shift keyed.");

		// all key bindings use control key, first
		switch(event.keyCode) {
			//console.log("keydownWatchdog: keyCode " + event.keyCode + ".");

			case 38: // up arrow
				loadImages();

				break;
			case 37: // left arrow
				if(!$("a[name='left-button']").hasClass("disabled")) {
					imageSelect('left');
					switchImageHeightLock();
				}

				break;
			case 39: // right arrow
				if(!$("a[name='right-button']").hasClass("disabled")) {
					imageSelect('right');
					switchImageHeightLock();
				}

				break;
			case 13: // enter
				$('#verification').modal('open');

				break;
			case 189: // minus (-)
				if(!$("#zoom-out-btn").hasClass("disabled"))
					zoom("out");

				break;
			case 187: // plus (+)
				if(!$("#zoom-in-btn").hasClass("disabled"))
					zoom("in");

				break;
			case 76: // the letter L
				if(zoomLevel != 1)
					switchImageHeightLock();

				break;
			default:
				console.log("keydownWatchdog: Non-defined key " + event.keyCode + " triggered.");
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
 * @returns nothing.
 */
function switchImageHeightLock() {

	if(imageHeightLocked) {
		$("#image-previewer").removeAttr("height");
		$("#image-previewer").attr("width", $("#image-previewer-holder").width() + "px");

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

};

var currentImage = 0, totalImages = 0, zoomLevel = 1;

/**
 * updateCounters()
 *
 * Reflect the counters directly above this function onto the web
 * page.
 *
 * @returns	nothing.
 */
function updateCounters() {

	$("#current-image").html(currentImage + 1);
	$("#total-images").html(totalImages);
	$("#zoom-level").html(zoomLevel);

};

/**
 * indexExistsIn(array arr, int i)
 *
 * Determines if an index exists in an array, because this is somehow
 * not a built-in function.
 *
 * @param	arr		is an array [] containing at least one element.
 * @param	i		is index.
 *
 * @returns true if an index, i, exists within array, arr.
 */
function indexExistsIn(arr, i) {

	if(i < arr.length && i >= 0)
		return true;

};

/**
 * showImage(int index)
 *
 * Put up an image in the viewer from imgs array at specific index.
 *
 * throws error if index below or beyond array elements.
 *
 * @param	index	the index of the image to display.
 *
 * @returns nothing.
 */
function showImage(index) {

	if(!indexExistsIn(imgs, index))
		throw "showImage(index): Index out of bounds error: " + index + ".";

	currentImage = index;

	$("#image-previewer").attr("src", "get/imgs/" + imgs[index]);
	$("#current-image").html(currentImage);

	updateCounters();

};

/**
 * imageSelect(string dir)
 *
 * dir in this function stands for direction.
 *
 * Moves "left" or "right" (dir:direction) by one image.
 *		  ^			^
 *
 * @param	dir		the direction to select images, either "left" or
 *					"right".
 *
 * @returns nothing.
 */
function imageSelect(dir) {

	switchImageHeightLock();

	// normal select
	var change = 0;

	if(dir == "left")
		change = -1;
	else if(dir == "right")
		change = 1;
	else
		throw "imageSelect(direction): Unknown cardinal horizontal direction '" + dir + "'";

	if(indexExistsIn(imgs, currentImage + change))
		showImage(currentImage + change);

	updateDirectionalButtons();

};

/**
 * updateDirectionalButtons()
 *
 * Updates the directional buttons for switching between images
 * appropriately.
 *
 * @returns nothing.
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

};

// image zoom

/**
 * updateImagePreviewDimensions(String dir)
 *
 * dir in this function stands for direction.
 *
 * Maintains the correct height and width pixel measurements for the
 * #image-previewer-container div before and after unlocking or locking
 * the image size ratio.
 *
 * @param	dir		the depth to zoom in the image to.
 *
 * @returns nothing.
 */
function updateImagePreviewDimensions(dir) {

	// fix container
	$("#image-previewer-holder").css({
		"width": $("#image-previewer-container").width(),
		"height": $("#specifications-pane-container").height()
	});

	// fix image itself
	if(zoomLevel == 1 && dir == "out") {

		$("#image-previewer").css(
			{
				"width": 'auto',
				"height": establishedLockHeight
			}
		);

	} else {

		var deltaZ = (zoomLevel/(zoomLimit/zoomFactor));

		// a = (a)ctual image dimensions
		var Wa = $('#image-previewer')[0].naturalWidth;
		var Ha = $('#image-previewer')[0].naturalHeight;

		// c = (c)ropper image dimensions (static)
		var Wc = $("#image-previewer-container").width();
		var Hc = $("#image-previewer-container").height();

		// s = scroll (l)eft/(t)op
		var Sl = $("#image-previewer-container").scrollLeft();
		var St = $("#image-previewer-container").scrollTop();

		// (old) size in background and (new) size in background
		var Wnew = $('#image-previewer')[0].naturalWidth * deltaZ;
		var Wold = $('#image-previewer').width();

		var Hnew = $('#image-previewer')[0].naturalHeight * deltaZ;
		var Hold = $('#image-previewer').height();

		// must set new width and height before scrolling
		$("#image-previewer").css({
			"width": Wnew,
			"height": Hnew
		});

		// (M)iddle (P)oint of current viewbox
		var MPx = (Sl + (Wc/2));
		var MPy = (St + (Hc/2));

		var Sx = Wnew/Wold;
		var Sy = Hnew/Hold;

		// new (M)iddle (P)oint of scroll box
		var MPxn = Sx * MPx;
		var MPyn = Sy * MPy;

		$("#image-previewer-container").scrollTop(
			MPyn - (Hc/2)
		);

		$("#image-previewer-container").scrollLeft(
			MPxn - (Wc/2)
		);

	}

};

/**
 * updateZoomButtons()
 *
 * Enables/disables the zoom in buttons, depending upon the zoomLevel.
 *
 * @returns nothing.
 */
function updateZoomButtons() {

	// zoom in
	if(zoomLevel == zoomLimit)
		$("#zoom-in-btn").addClass("disabled");
	else
		$("#zoom-in-btn").removeClass("disabled");

	// zoom out
	if(zoomLevel == 1)
		$("#zoom-out-btn").addClass("disabled");
	else
		$("#zoom-out-btn").removeClass("disabled");;

	updateCounters();

	// disable image aspect ratio lock
	if(zoomLevel > 1 && zoomLevel <= zoomLimit) {
		$("#size-lock-button").addClass("disabled");
		$("#size-lock-button").addClass("shift-lock-icon");
	} else {
		$("#size-lock-button").removeClass("disabled");
		$("#size-lock-button").removeClass("shift-lock-icon");
	}

};

var zoomLevel = 1, zoomFactor = 1.5, zoomLimit = 10;

/**
 * zoom(String dir)
 *
 * dir in this function stands for direction.
 *
 * zoom("in") zooms in on the image-preview by 1x.
 * zoom("out") zooms out of the image-preview by 1x.
 *
 * No preconditions.
 *
 * zoomLevel is > 0 and <= zoomLimit
 *
 * The magnification formula is defined as such:
 *		   zoomLevel
 *  ----------------------  =  deltaZ
 *   zoomLimit/zoomFactor
 *
 *  deltaZ * Width of the actual image = new Width
 *  deltaZ * Height of the actual image = new Height
 *
 * @param	dir		the depth of the zoom, with 1 being regular fit, and
 *					10 being a 10x zoom.
 *
 * @returns nothing.
 */
function zoom(dir) {

	// hide overflow when zooming back in to original
	if(zoomLevel == 2 && dir == "out")
		$("#image-previewer-container").css(
			{
				"overflow": 'scroll',
				"height": establishedLockHeight,
				"width": 'auto'
			}
		);

	// add overflow when zooming out from original
	if(zoomLevel == 1 && dir == "in")
		$("#image-previewer-container").css({"overflow": 'auto'});

	if(dir == "in") {
		if(zoomLevel < zoomLimit) {
			// zoom in
			zoomLevel++;

			updateImagePreviewDimensions(dir);
		}
	} else if(dir == "out") {
		if(zoomLevel > 0) {
			// zoom out
			zoomLevel--;

			updateImagePreviewDimensions(dir);
		}
	}

	updateZoomButtons();

};

// target submission

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
 *
 * @returns nothing.
 */
function loadCropPreview() {

	// display crop preview
	$(document).ready(function() {

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

		$("#crop-previewer").css({
			"border": "1px solid black",

			"background-image": "url('imgs/" + imgs[currentImage] + "')",
			"background-repeat": "no-repeat",
			"background-attachment": "scroll",

			"background-size": transformedW + "px " + transformedH + "px",
			"background-position":
				"-" + (transformed_topLeftX + 50) + "px " +
				"-" + (transformed_topLeftY + 34) + "px"
		});

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

};

/**
 * submitTarget()
 *
 * Triggered by Crop Image Previewer modal in MTS.
 *
 * Posts an AJAX request to back-end flask script the details of the crop, not
 * the actual crop itself. This also pushes the crop data (shape, color, etc.)
 *
 * Automatically determines the target type based on which target type is
 * currently selected.
 *
 * @returns nothing.
 */
function submitTarget() {

	var targetData;

	if( $("a[href='#standard-target']").hasClass("active") ) {
		// if a standard target
		targetData = {
			type: "standard",
			ignoreDuplicates: "false",

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
		};
	} else if( $("a[href='#emergent-target']").hasClass("active") ) {
		// if an emergent target
		targetData = {
			type: "emergent",
			ignoreDuplicates: "false",

			targetTopLeftX: cropData.targetTopLeftX,
			targetTopLeftY: cropData.targetTopLeftY,

			targetBottomRightX: cropData.targetBottomRightX,
			targetBottomRightY: cropData.targetBottomRightY,

			imageFilename: cropData.imageFilename,

			description: $("#emergent-description").val(),
		};
	} else {
		var $toastContent = $('<span><b>FAILURE:</b> Client-side failure on submitting target.</span>');

		Materialize.toast($toastContent);
		console.log("submitTarget(): Unable to determine selected target type.");

		throw "submitTarget(): Indeterminate error";
	}

	$.ajax({
		url: "/post/target",
		method: "POST",
		timeout: 3000,

		data: targetData,

		dataType: "json",

		success: function(data) {
			// target is potential duplicate; prompt user
			if(data[0] != null) {
				duplicatedTargetsInfo = [];

				data.forEach(function(item) {
					if(item["duplicatesPossible"] == null) // if not a duplicatesPossible notice
						duplicatedTargetsInfo.push(item) // add duplicate target info

					duplicateTargets(duplicatedTargetsInfo);
				});
			}

			// target submitted and was successful
			var $toastContent = $('<span><b>SUCCESS:</b> Sent target to backend script.</span>').add($('<button class="btn-flat toast-action" onclick="( $(\'.toast\').first()[0] ).M_Toast.remove();">X</button>'));

			Materialize.toast($toastContent);

			console.log("submitTarget(): ajax data:")
			console.log(data);

			updateCounters();
		},

		error: function(data) {
			// server side error
			var $toastContent = $('<span><b>FAILURE:</b> Unable to send target; See console.</span>');

			Materialize.toast($toastContent);

			console.log("submitTarget(): ajax data:");
			console.log(data);
		}
	});

};

duplicatedTargetsInfo = [
	{
		name: "target002",
		matches: 0,

		type: "standard",

		imageURL: "get/crop/291015.jpg",
		geo: "38.38093, 78.12923",
		shape: "triangle",
		shapeColor: "blue",
		textColor: "red",
		alphanumeric: "Z"
	},
	{
		name: "target003",
		matches: 2,

		type: "standard",

		imageURL: "get/crop/291012.jpg",
		geo: "38.38109, 78.12915",
		shape: "rectangle",
		shapeColor: "blue",
		textColor: "blue",
		alphanumeric: "G"
	}
];

/**
 * duplicateTargets(Array info)
 *
 * Open and fill the duplicate targets modal with submitted target info.
 * passed from info.
 *
 * @param	info	the array of duplicateTargetsInfo in the format of:
 *					[
 *						{
 *							name: "target001",
 *							matches: 3, // characteristics that match
 *
 * 							imageURL: "get/crop/001.jpg",
 *							geo: "38.38101 N, 78.12919 W",
 *							shape: "rectangle",
 *							shapeColor: "red",
 *							textColor: "blue",
 *							alphanumeric: "G"
 *						},
 *						...
 *					]
 *
 * @returns nothing.
 */
function duplicateTargets(info) {

	// reset
	$("#duplicate-target-collection").html("");
	firstActive = " active";

	// @TODO: add sort by number of matches per target
	// determine number of matches and sort by them
	//newDuplicatedTargetsInfo = [];
	//newDuplicatedTargetsInfo.forEach(function(item) {
	//})
	//dulpicatedTargetsInfo = newDuplicatedTargetsInfo;

	// fill collection
	duplicatedTargetsInfo.forEach(function(item, index) {
		var badgeColor = "";

		switch(item.matches) {
			case 4:
				badgeColor = "red";
				break;
			case 3:
				badgeColor = "orange";
				break;
			case 2:
				badgeColor = "yellow darken-2";
				break;
			case 1:
				badgeColor = "green";
				break;
			default:
				badgeColor = "blue";
				break;
		}

		match_grammar = "";

		if(item.matches > 1)
			match_grammar = "Matches";
		else
			match_grammar = "Match"

		$("#duplicate-target-collection").html(
			$("#duplicate-target-collection").html() + "<a id='dt-i-" + index +
			"' href='#!' class='collection-item" + firstActive +
			"' onclick='showDuplicateTarget(" + index + ")'>" + item.name +
			"<span class='badge'>" + (item.type).toUpperCase() + "</span> <span class='new badge " + badgeColor + "' data-badge-caption='" + match_grammar + "'>" + item.matches +"</span></a>"
		);

		// set first item to active
		if(firstActive.length > 0) {
			showDuplicateTarget(0);
			firstActive = "";
		}

	});

	// show cropped selection
	$("#duplicate-target-pending-image").html($("#crop-previewer").clone()).attr("transform", "scale(.5)");
	/*$("#cropper-holder-image").attr("src", "get/imgs/" + cropData.imageFilename);

	var pending_potential_duplicate = document.getElementById("cropper-holder-image");

	var cropper = new Cropper(pending_potential_duplicate, {
		autoCrop: true,
		aspectRatio: 1 / 1,
		viewMode: 1
	});

	$(document).ready(function() {
		setTimeout(function() {
			cropper.moveTo(1005, -50);
			cropper.zoom(2);

			$("#crop-duplicate-preview").html(
				cropper.getCroppedCanvas({
				   	width: 160,
				   	height: 90,
				    minWidth: 256,
				    minHeight: 256,
				  	maxWidth: 4096,
				  	maxHeight: 4096,
				   	fillColor: '#fff',
				   	imageSmoothingEnabled: false,
				   	imageSmoothingQuality: 'high',
				})
			);

			$("#cropper-holder").css({
				"display": "none"
		    });
		}, 100);
	});*/

	/*
	$("#crop-duplicate-preview").attr("src", "/get/imgs/" + cropData.imageFilename);

	$("#crop-duplicate-preview").attr(
		"src",
		$("#crop-duplicate-preview").cropper(
			"getCroppedCanvas",
			{
				"width": 100,
				"height": 100,
			}
		)
	)*/

	// list characteristics
	if( $("a[href='#standard-target']").hasClass("active") ) { // if standard target
		$("#duplicate-target-pending-shape").html(capitalizeFirstLetter($("#target-shape").val()));
		$("#duplicate-target-pending-shape-color").html(capitalizeFirstLetter($("#target-color").val()));
		$("#duplicate-target-pending-text-color").html(capitalizeFirstLetter($("#content-color").val()));
		$("#duplicate-target-pending-alphanumeric-content").html($("#target-content").val());
	} else if( $("a[href='#emergent-target']").hasClass("active") ) { // if emergent target
		$("#duplicate-target-pending-shape").html("<i>N/a</i>");
		$("#duplicate-target-pending-shape-color").html("<i>N/a</i>");
		$("#duplicate-target-pending-text-color").html("<i>N/a</i>");
		$("#duplicate-target-pending-alphanumeric-content").html("<i>N/a</i>");
	}

	// fix grammar on notice text
	if(info.length > 1) {
		$("#dt-g-0").html("some");
		$("#dt-g-1").html("targets");
	} else {
		$("#dt-g-0").html("a");
		$("#dt-g-1").html("target");
	}

	// show
	$("#duplicate-target").modal("open");

};

/**
 * showDuplicateTarget(int index)
 *
 * Displays a selected duplicate target on the potential match
 * visualizer inside of the Duplicate Targets modal.
 *
 * @param	index	the index of the duplcate target in
 *					duplicateTargetsInfo.
 *
 * @throws	Error	index is not a valid duplicate target. out of
 *						bounds.
 *
 * @returns nothing.
 */
function showDuplicateTarget(index) {

	// update collection
	duplicatedTargetsInfo.forEach(function(item, i) {

		$("#dt-i-" + i).removeClass("active");

	});

	$("#dt-i-" + index).addClass("active");

	// update table
	$("#duplicate-target-compare-image").html("<img src='" + duplicatedTargetsInfo[index].imageURL + "'>");

	// handle for different target types
	if(duplicatedTargetsInfo[index].type == "standard") {
		$("#duplicate-target-compare-shape").html(capitalizeFirstLetter(duplicatedTargetsInfo[index].shape));
		$("#duplicate-target-compare-shape-color").html(capitalizeFirstLetter(duplicatedTargetsInfo[index].shapeColor));
		$("#duplicate-target-compare-text-color").html(capitalizeFirstLetter(duplicatedTargetsInfo[index].textColor));
		$("#duplicate-target-compare-alphanumeric-content").html(duplicatedTargetsInfo[index].alphanumeric);
	} else if(duplicatedTargetsInfo[index].type == "emergent") {
		$("#duplicate-target-compare-shape").html("<i>N/a</i>");
		$("#duplicate-target-compare-shape-color").html("<i>N/a</i>");
		$("#duplicate-target-compare-text-color").html("<i>N/a</i>");
		$("#duplicate-target-compare-alphanumeric-content").html("<i>N/a</i>");
	}

	// check and highlight the similarities and differences
	fieldsToCheck = [
		"#duplicate-target*shape",
		"#duplicate-target*shape-color",
		"#duplicate-target*text-color",
		"#duplicate-target*alphanumeric-content"
	];

	fieldsToCheck.forEach(function(item) {

		if(duplicatedTargetsInfo[index].type == "emergent") {
			$(item.replace("*", "-")).removeClass("green red");
			return null;
		}

		if( ($(item.replace("*", "-pending-"))).html() == $(item.replace("*", "-compare-")).html() ) { // if they are the same
			$(item.replace("*", "-")).removeClass("green");
			$(item.replace("*", "-")).addClass("red");
			$(item.replace("*", "-identifier-")).html("Same");
		} else { // if they are different
			$(item.replace("*", "-")).removeClass("red");
			$(item.replace("*", "-")).addClass("green");
			$(item.replace("*", "-identifier-")).html("Different");
		}

	});

};

// control panel code

var refresh = null;

/**
 * switchControlPanelRefresh()
 *
 * Enable or disable the automatic control panel refresh.
 *
 * @returns nothing.
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

};

// front-to-backend code

/**
 * statusDisplay(String programName, String status)
 *
 * Front-end update function that's used by statusPush() and statusGet().
 *
 * Updates the Control Panel slide with the data that was received by
 * the back-end script.
 *
 * # TODO: expand
 * @param	programName		"interop", "img"
 * @param	data			...
 *
 * @returns nothing.
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

			$(ref + "-power-button").removeClass("green").addClass("red");
			$(ref + "-power-button").attr("onclick", "statusPush('" + programName + "', 'off');");
		}

	} else if(data["status"] == "disconnected") { // disconnected

		if(!$(ref + "-light").hasClass("red")) {
			$(ref + "-light").removeClass("green").addClass("red");
			$(ref + "-light-text").html("Disconnected");

			$(ref + "-power-button").removeClass("red").addClass("green");
			$(ref + "-power-button").attr("onclick", "statusPush('" + programName + "', 'on');");
		}

	}

};

/**
 * statusPush(String process, String cmd)
 *
 * Turn on or off a subprocess, with the subprocessesing being:
 *	- "interop-connection",
 *	- "sda", and
 *	- "image-processing"
 * by posting an AJAX request to the back-end script.
 *
 * @returns nothing.
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

};

/**
 * statusGet()
 *
 * Retrieves the status informaition of the different subprocesses for the
 * control panel.
 *
 * @param	programName		either "interop", "img_proc", or "sda".
 *
 * @returns nothing.
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

};

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
 * @throws nothing.
 *
 * @returns nothing.
 */
function loadImages() {

	$("#loading-bar").removeClass("hide");

	$.ajax({
		url: "get/imgs",

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
				keys: false,
				fadeSpeed: 0.4,
				//zIndex: -1,

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

			// needs to be doubled
			switchImageHeightLock();

			// indicate
			$("#loading-bar").addClass("hide");
			Materialize.toast('Images successfully loaded.', 2400);
		},

		error:function(data) {
			// indicate
			$("#loading-bar").addClass("hide");
			Materialize.toast('Failed to load images, check console.', 4000);

			console.log("loadImages(): Unknown connection error, see:");
			console.log(data);
		}
	});

};

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

	$("#zoom-in-btn").removeClass("disabled");
	$("#zoom-out-btn").removeClass("disabled");

	$("#emergent-description").removeAttr("disabled");

	updateZoomButtons();

};

/**
 * resetWaypoints()
 *
 * Opens a dialog to confirm a redownload/resetting of the waypoints sent to the
 * drone.
 *
 * @returns nothing
 */
function resetWaypoints() { $("#reset-waypoints").modal("open") }

/**
 * resetWaypoints()
 *
 * Redownloads/resets the waypoints sent to the drone.
 *
 * @returns nothing.
 */
function resetWaypointsConfirm() {

	$.ajax({
		url: "/get/waypoints/reset",
		method: "GET",
		timeout: 1000,
		async: true,

		dataType: "json",

		success: function(data) {
			if(data["request_status"] == "success") {
				Materialize.toast("Reset waypoints succesful.", 1000);
			} else if(data["request_status"] == "failure") {
				Materialize.toast("See console: Failed to reset waypoints.", 1000);
				console.log("resetWaypointsConfirm(): Server-side failure, see data below:");
				console.log(data);
			} else {
				Materialize.toast("See console: Received unknown status for waypoint reset.");
				console.log("resetWaypointsConfirm(): Received unknown status, see data below:");
				console.log(data);
			}
		},

		error: function(data) {
			// server side error
			Materialize.toast('See console: /post/waypoints/reset failed.', 1000);
			console.log("resetWaypointsConfirm(): /post/waypoints/reset failed, see data below:");
			console.log(data);
		}
	});

}

/**
 * setCompassDirection(int degrees)
 *
 * Sets the direction that the compass is point in the Image Previewer and
 * Cropper slide.
 *
 * @param	degrees		Degrees as an integer or double.
 *
 * @returns nothing.
 */
function setCompassDirection(degrees) {

	$("#compass-pointer").css("transform", "rotate(" + degrees + "deg)");
	$("#compass-number").html(degrees);

}

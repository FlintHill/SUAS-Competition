<?php

	# change "robo" and "password" to their respective username and password
	$link = mysqli_connect("localhost", "robo", "password", "tile");

	$query = $link->query("SELECT SQL_CACHE defaults, image FROM `tiles` WHERE ".
		"`z`=".$_GET['z']." AND `x`=".$_GET['x']." AND `y`=".$_GET['y']);

	if(!$query) {
		http_response_code(500);
		echo "The connection to the database failed";
	}

	header('Content-Type: image/png');

	if($query->num_rows === 0) {
		http_response_code(404);
		echo file_get_contents("missing.png");
	} else {
		$result = $query->fetch_array(MYSQLI_NUM);

		if($result[0] >= 0) {
			echo $link->query("SELECT SQL_CACHE image FROM `defaults` WHERE ".
				"`id`=".$result[0])->fetch_array(MYSQLI_NUM)[0];
		} else {
			echo $result[1];
		}
	}

?>

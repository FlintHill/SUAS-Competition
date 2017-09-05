<?php

	define("ROOT_DIR", "/Apache24/htdocs/tile/");

	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);


	$link = mysqli_connect("localhost", "root", "robotics", "tile");

	$query = $link->query("SELECT * FROM `defaults` WHERE 1");

	$defaults = array();

	while($row = $query->fetch_assoc()) {
		array_push($defaults, $row);
	}

	function listDir($dir) {
		$array = array_diff(scandir(ROOT_DIR.$dir), array('..', '.', '.htaccess', 'handler.php', 'loader.php', 'missing.png'));

		foreach($array as &$arr) {
			if(strpos($arr, ".") != false)
			$arr = substr($arr, 0, strpos($arr, "."));
		}

		return $array;
	}

	$files = array();

	for($z = min(listDir("")); $z <= max(listDir("")); $z++) {

		$dir = listDir($z."/");

		for($x = min($dir); $x <= max($dir); $x++) {

			if(!file_exists(ROOT_DIR.$z."/".$x."/"))
				continue;

			$childDir = listDir($z."/".$x."/");

			for($y = min($childDir); $y <= max($childDir); $y++) {

				$imagePath = ROOT_DIR.$z."/".$x."/".$y.".png";

				if(file_exists($imagePath)) {
					$id = $link->query("SELECT MAX(id) FROM `tiles`")->fetch_array(MYSQLI_NUM)[0] + 1;

					$query = "INSERT INTO `tiles` (`id`, `z`, `x`, `y`, `defaults`, `image`) ".
						"VALUES ('".$id."', '".$z."', '".$x."', '".$y."', '-1', '".$link->real_escape_string(file_get_contents($imagePath))."')";

					// compare with defaults
					for($i = 0; $i < count($defaults); $i++) {
						if(sha1_file($imagePath) == $defaults[$i]["sha1"]) {
							$query = "INSERT INTO `tiles` (`id`, `z`, `x`, `y`, `defaults`, `image`) ".
								"VALUES ('".$id."', '".$z."', '".$x."', '".$y."', '".$i."', '')";
							break; // this might break the code
						}
					}

					$result = $link->query($query);
				}

			}

		}

	}

	echo "<pre>";
	print_r($files);
	echo "</pre>";

?>

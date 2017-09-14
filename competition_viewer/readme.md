# SDA Viewer #

This page details the setup, function, and operation of the Sense, Detect, and Avoid viewer.

---

## Viewer ##

This application allows us to view, from any modern web browser, the current
set of obstacles and the drone's position via websockets in realtime.

The details of the program are enumerated below.

### About ###

Using a combination of an [Apache webserver](https://www.apache.org/) with a [PHP](https://php.net/) extension (and a [MySQLi library](https://php.net/manual/en/book.mysqli.php) included), [MySQL database](https://www.mysql.com/), Javascript (consisting of [JQuery](https://jquery.com/) and [LeafletJS](http://leafletjs.com/) libraries included), we have created viewer that allows see—in realtime—the position of our team's drone, obstacles, waypoints, and more.

This is used by Flint Hill's Animus Ferus Team in the AUVSI SUAS Competition.

### Setup and Configuration ###

The rough instructions on how to start up and configure the viewer are detailed below:

**Note:** It's recommended that you install [WinRAR](http://www.rarlab.com/download.htm) to simplify

1. Download and install into the root directory, `C:/` (preferably in 64-bit, if using a 64-bit OS):
	- [Apache 2.4](https://www.apachelounge.com/download/)
		- Download the most recent windows binary that's labeled `Win64`
		- Open the downloaded archive and drag all the contents to the root of your computer.

		The folder structure should look like `C:/Apache24/` where the `Apache24` directory contains the `htdocs`, and other Apache associated directories.
		- Open a command prompt window, and cd into `C:/Apache24/bin` then execute the command `httpd -k install`, and `http -k start`
		- Open a browser window, and navigate to `localhost`. You should be able to see the status message `It works!`.
	- [PHP 7](http://windows.php.net/download#php-7.1)
		- Download the most recent version of PHP that contains the text `x64 Non Thread Safe` in the title.
		- Drag the contents of downloaded archive into the root of your computer.

		The folder structure should look like `C:/php/` where the `php` directory contains the `lib` directory, and other PHP associated directories.
	- [MySQL](https://dev.mysql.com/downloads/mysql/)
		- Open the installer and choose all the default options.
			- Remember to save the root account password on a piece of paper.
2. Configure the Apache Server:
	- Open `Apache24/bin/httpd.conf`
		- In the `<Directory "C:/Apache24/htdocs">` field, change  `AllowOverride None` to `AllowOverride all`.

		- Change `DirectoryIndex index.html` to `DirectoryIndex index.php index.html`

		- Enable the PHP module by adding the following lines to the end of the configuration file:

		`LoadModule php5_module "C:/PHP/php5apache2_4.dll"
		AddHandler application/x-httpd-php .php
		PHPIniDir C:/PHP`
	- Save and exit the `httpd.conf` file.

3. Configure PHP:
	- Navigate to `C:/PHP`, and rename `php.ini-development` to `php.ini`.
	- Open the newly renamed file.
		- Uncomment the line `#extension=mysqli.dll` to `extension=mysqli.dll`
	- Save and exit the `php.ini` file.
4. Configure MySQL:
	- Download [phpmyadmin](https://www.phpmyadmin.net/), and drag the contents of the download archive to the `C:/Apache24/htdocs/` directory.

	The folder inside the archive usually has some complicated name, so it is **strongly recommended** to rename the directory to simply `phpmyadmin`, so that the folder structure looks like `C:/Apache24/htdocs/phpmyadmin/`.
	- In a web browser, navigate to `localhost/phpmyadmin` (or if you did not change the name of the phpmyadmin directory, replace phpmyadmin with whatever is the name of the directory in `htdocs`), and type in the username `root`, and the password of the root user that you set during the MySQL installation.
		- If you do not remember the password you set, you may need to reinstall MySQL.
	- Create a new MySQL database, called `tile`.
	- Open the `tile` database, if it is not already open in phpmyadmin.
	- Create a new table within the `tile` database, called `tiles` with the following column structure:
		- Row 1 -> name: `id`, type: `INT`, index: `PRIMARY` (a pop-up box will appear, just hit ok.)
		- Row 2 -> name: `z`, type: `INT`.
		- Row 3 -> name: `x`, type: `INT`.
		- Row 4 -> name: `y`, type: `INT`.
		- Row 5 -> name: `defaults`, type: `INT`, default: `As defined: -1`.
		- Row 6 -> name: `image`, type: `blob`.
	- Going back to the `SUAS-Competition` github repo, open `sda_viewer/tile/resources/`, and within phpmyadmin, import the file `defaults.sql` while still within the `tile` database.
	- Go into `sda_viewer/tile/scripts/` and run `download.py`, and enter the coordinates of your current position. The script will stop once it has downloaded all the map tiles. **This may take some time, so be patient.**
	- Move the tile folder, and the script named `import.php` that is also within the `scripts` directory to `htdocs`, and then open `localhost/import.php` on a web browser.
		- This will load all the images into the MySQL database. **This should take no longer than 30 seconds.**
	- To ensure that the import script worked successfully, open the `tiles` table in phpmyadmin, and check to see if there are rows with different and unique z, x, and y rows with the blob image size varying between the different row entries.
		- You can also navigate to `localhost/sda/viewer/` in your browser, and if you see tiles, **then you have successfully setup the MySQL server.**
5. Hit the Windows key, and in the menu that appears, type in `services.msc`, and hit enter.
	- In the window that opens, right click on the `Apache2.4` (Apache Server) service, and select `Restart`.
	- Right click on the `Apache2.4` process again and click `Properties`. Change `Startup type` to `Automatic`. This will tell Windows to launch the Apache server every time the computer restarts, or boots up from a shutdown.
6. Drop all the files within this `sda_viewer/` directory into `C:/Apache24/htdocs/`
	- Edit `tile/index.php` to the correct username and password to the MySQL account that you setup earlier.
7. You are finished.

You should be able to navigate to `localhost/sda/viewer/`, and see map tiles in the background. Additionally, if you run the dummy websocket server in `sda/viewer/python/demo-websocket/server.py`, and connect to it in the viewer with the IP address `localhost`, you should also be able to see map points, such as drone position, flight boundaries, and more.

### Interop. Server Specification ###

This section details the exact information retrieved from the AUVSI SUAS' Interoperability Server, based off the specifications that competition managers detail here:

http://auvsi-suas-competition-interoperability-system.readthedocs.io/en/latest/specification.html

The Interop. server is not used directly by the viewer—as the Interop. mission and obstacle data is supplied through the websocket—, however, the format of the data, as described in the link above, is what is expected to be received by the viewer.

The exact format expected is described below with the websocket server JSON response data, in the field labeled `interop. server info`.

### WebSocket Server Specification ###

This section regards the information that needs to be transmitted from a WebSocket server in order to be used in the viewer.

A websocket is the primary and only connection that the viewer needs to establish in order to obtain the drone's current position, obstacle data, and other relevant mission points.

An **example response** that a websocket must return is displayed below:

```
{
    // "topical" information (drone data)
    "alt":0.00,
    "dir":3,
    "speed":0.0,
    "velocity":0.0316227766017,
    "lat":38.870304,
    "long":-77.321404,

    // interop. server info (obstacles, points, flyzones, etc.)
    "0": {
        "stationary_obstacles":[
            {
                "latitude":38.87152778,
                "cylinder_height":780.0,
                "cylinder_radius":50.0,
                "longitude":-77.32138889
            }
        ],
        "moving_obstacles":[ ... ],
        "fly_zones":[
            {
                "altitude_msl_max":835.0,
				"altitude_msl_min":530.0
                "boundary_pts":[
                    {
                        "latitude":38.87291667,
                        "order":1,
                        "longitude":-77.32208333
                    },
                    ...
                ],
            }
        ],
        "mission_waypoints":[
            {
                "latitude":38.8725,
                "altitude_msl":780.0,
                "order":12,
                "longitude":-77.32083333
            },
            ...
        ],
        "search_grid_points":[
            {
                "latitude":38.87263889,
                "altitude_msl":430.0,
                "order":8,
                "longitude":-77.32208333
            },
            ...
        ],
		"off_axis_target_pos":{
            "latitude":38.87069444,
            "longitude":-77.32152778
        },
        "emergent_last_known_pos":{ ... },
        "home_pos":{ ... },
        "air_drop_pos":{ .. }
    }
}
```

**Note:** This example response is available in it's unedited entirety at `viewer/python/demo-websocket/data_example.json` (relative to this readme).

The information, much like the example response above, is retrieved after a dummy message is sent off. In our case, we just send a String, `update`. This message is intended to provoke a response from the websocket. Where the websocket then returns the information immediately afterwards.

The following information is **required** for the viewer to operate:

| Short | Full Field Name | Type              | Description |
| :---- | :-------------- | :---------------- | :---------- |
| 0  | Interop. Mission Data | (Mixed) ___JSON element___  | All the mission data that the Interop. server provides on the API endpoint `api/missions`, as well as `api/obstacles` included within the initial `api/missions` JSON data. |
| alt   | Altitude | (Float/Double) ___Decimal___ | Absolute distance from the ground, not sea level, to the drone. |
| dir   | Direction | (Float/Double) ___Degrees___ | In degrees, from 0 to 360 inclusive, where the drone is pointing to relative to the north pole. |
| speed | Speed | (Float/Double) ___Decimal___ | The change, or delta, in the drone's current latitude and longitude from it's last. |
| velocity | Velocity | _same as above_ | The change, or delta, in the drone's current position (lat, long, alt) from it's last. |
| lat   | Latitude | _same as above_   | The difference from the equator to the drone's current latitude in decimal degrees.
| long  | Longitude  | _same as above_   | The difference from the Prime Meridian to the drone's current longitude in decimal degrees. |

All of this information, except 0 and altitude, is critical in displaying the drone's current position.

### Features not yet implemented ###

There are several features that have not been implemented:

 - Currently, the altitude is not taken into account with regards to obstacles. If an obstacle does not exist on the same altitude as the drone, then ideally, the obstacle would be made either semi or fully transparent. This is a feature that needs to implemented at a later date.
 - The lack of error support in websocket connections needs to be addressed.
 - Add retina versions of marker icons.
 - Change the drone position icon to a classic GPS triangle icon that correctly indicates the direction of the drone.

## Tile Server ##

The details of the tile server are detailed below.

The setup of the tile server is included in the set of instructions above. But, to summarize the instructions: You need to download map tiles from an online resource (such as OpenStreetMap), and import them into a MySQL database.

The tile server is required to serve the map tiles that appear in the background of the viewer offline, because at the competition, an internet connection will not be provided.

### Downloading the tiles ###

Map tiles are typically copyrighted, or have some restrictions regarding how many map tiles you can obtain, and how you can use them. Because of these limitations, we chose to use [OpenStreetMap](http://osm.org), a free and open source map project contributed to by many people around the world.

For our two relevant locations—FlintHill School grounds and the Pax River Naval Air Station—there is a rich amount of map data including the location of forests, trails, roads, structures, and other relevant data that makes the OSM map data suitable.

In order to have a functioning map tile server, you of course need the map tiles themselves in order to serve.

We simply use a crude script, `download.py`, within `tile/scripts`, where we input a latitude, longitude, and zoom level, and the script starts downloading the tiles from OSM.

Perhaps there is a more elegant solution to retrieve the map tiles in way that would allow future map tile updates, but this was attempted for several months with no success.

Simply,

1. Run `tile/scripts/download.py`
	- Input your current latitude and longitude.
		- You can do this by going to Google Maps, clicking on your current location, and using the lat. and long. that appears at the bottom of the screen.
	- Input the desired zoomed level.
		- _If you do not know,_ simply enter `0`.
	- Ensure that the computer that is running the script will not shut off (either by going into the Power settings of your device), as this will take some time to complete.
2. A new folder should appear, called `tiles`, within, you should see several sub-folders `0`, `1`, `2`, `3`, and so on and so forth.

Now you need to import the tiles into the database.

### Importing the tiles into MySQL ###

Now that you have the map tiles downloaded, you will now need to import them into a MySQL database in order for the tiles to be properly served.

1. Move the `tiles` folder into `htdocs` (Apache Web Root.)
	- Check to see that the folder structure is `htdocs/tiles/[several folders, numbers 0-18]`
2. Ensure that the MySQL username and password inside the `tile/scripts/loader.php` script has the same username and password as your MySQL installation by logging into phpmyadmin with those credentials.
3. Go to a web browser, and enter `localhost/tile/scripts/loader.php`.
	- You shouldn't see anything happen immediately. It takes awhile to process all the images into the database. After the script is done, it will print out all the images uploaded to the database.
	- If the script did not work, ensure that the login, ROOT_DIR, or no other variables are incorrect.
4. While in your web browser, goto `localhost/phpmyadmin/`, login, and open the `tile` database, and check to see if the `tiles` table is populated with map tiles.
	- It should be obvious that there are several thousand rows in the table now, while previously, there should have been 0 rows in the table.
5. You have successfully uploaded the map tiles to the database.

Now all you need to do is complete the final sub-section of steps.

### Checking the tile server ###

This is the last section, congratulations, you made it. Now all you need to do is:

1. Open a web browser.
2. Navigate to `localhost/competition/viewer/`.
3. If everything went off without a hitch, you should see a map of the world, Flint Hill School and it's surrounding area, or the Patuxent Naval Airbase.
	- If the map tiles do not appear, check the previous steps to ensure that you completed them exactly and in the correct order.

You are finished.

---

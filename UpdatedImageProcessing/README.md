# Image Processing API

Part of the AUVSI SUAS Competition is a section called ODLC: Object Detection, Localization, and Classification. It is—in essence—finding targets on the ground from our drone in the air, determining it's geolocation based on the drone's position, and specifying the targets color, shape, and alphanumeric (text or number) content and color.

--

To install UpdatedImageProcessing as a package, from outside this directory, run: ```sudo -H pip install /UpdatedImageProcessing/ -U```.

If this does not work, it's recommended that you use `pip2.7` instead of `pip`.

--

A test for the ColorClassifer is `/tests/non_nose_tests/test_imgproc_color_classifier`

--

## ColorClassifier(img)

*img:* An opened PIL (Python Image Library) image.

Constructor.

*returns:* Nothing.

### get_color()

Gets the color of the background and text inside a target, in that order.

See section 3 for code source:
	[`https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/
	py_kmeans_opencv/py_kmeans_opencv.html`](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/
	py_kmeans_opencv/py_kmeans_opencv.html)

*returns:* 

```
	Two element list, where the first element is the shape color, and the 
	second element is the text color. 
		Ex:		["red", "green"] or, simply: 
				[<background color>, <text color>]
```
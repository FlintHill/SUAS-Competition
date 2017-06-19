# SUAS-Competition

Flint Hill School's code for the Student Unmanned Aerial Systems competition.

## License Information
Copyright 2017 Vale Tolpegin, Peter Hussisian, James Villamerette

Licensed under the MIT License. Please see the LICENSE file for more information

## Installation

### Installing OpenCV -- Mac OS X

OpenCV must be installed for this project to work. To install OpenCV's latest release, use Homebrew:

```
brew install opencv3 --with-tbb --with-cuda --with-contrib
```

This is a long process. After it is completed, you will have to link the python libraries. Find the generated ```cv2.so``` file, then copy it. Next, identify your local python instance's site-packages repository. Finally, copy the ```cv2.so``` file into the site-packages directory.

To test the installation, simply enter a quick command into terminal

```
python -c 'import cv2; print(cv2.__version__)'
```

This should print something like ```3.1.0```. If you get an error, that means that you did not install OpenCV correctly.

## Usage

### Using MAVProxy

To run MAVProxy, find the ID of the radio module (run ```ls /dev/``` and find the name of the ```usbserial``` device corresponding to the radio module) and then run the following command:

```
sudo python mavproxy.py --console --master=/dev/tty.usbserial-DEVICE_ID --out=tcpin:127.0.0.1:14551 --out=tcpin:0.0.0.0:14550
```

Assuming the ```python``` command references a Python 2.7.13 installation

### Using GCS

To run the Client script, cd into the ```gcs``` directory, then run

```
python client.py
```

Ensure that the version of Python you are using is 2.7.x. If attempting to use Python 3, the program will crash with a Timeout command.

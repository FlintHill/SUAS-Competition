# SUAS-Competition

[![Documentation Status](https://readthedocs.org/projects/suas-competition/badge/?version=latest)](http://suas-competition.readthedocs.io/en/latest/?badge=latest)


Flint Hill School's code for the Student Unmanned Aerial Systems competition.

## License Information
Copyright 2016-2017 Vale Tolpegin, Peter Hussisian, James Villamerette

Licensed under the MIT License. Please see the LICENSE file for more information

## Installation

### Installing Python

### Installing OpenCV -- Raspberry Pi

*NOTE This tab of instructions does NOT apply to OpenCV 3 nor Python3, and so will not work with the current system*

This project requires OpenCV to be built and compiled. The below code is only usable for Raspberry Pis. Other installation tutorials can be found online.

```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get -y install build-essential cmake cmake-curses-gui pkg-config libpng12-0 libpng12-dev libpng++-dev libpng3 libpnglite-dev zlib1g-dbg zlib1g zlib1g-dev pngtools libtiff4-dev libtiff4 libtiffxx0c2 libtiff-tools libeigen3-dev
sudo apt-get -y install libjpeg8 libjpeg8-dev libjpeg8-dbg libjpeg-progs ffmpeg libavcodec-dev libavcodec53 libavformat53 libavformat-dev libgstreamer0.10-0-dbg libgstreamer0.10-0 libgstreamer0.10-dev libxine1-ffmpeg libxine-dev libxine1-bin libunicap2 libunicap2-dev swig libv4l-0 libv4l-dev python-numpy libpython2.6 python-dev python2.6-dev libgtk2.0-dev

wget https://github.com/Itseez/opencv/archive/2.4.11.tar.gz
cd 2.4.11
mkdir release
cd release
ccmake ../
```

At this point, you will have to press 'c' to configure, and then once more to finish. Finally, press 'g' to generate the configuration file. Then, run the following.

```
sudo make -j4
sudo make install -j4
```

This will take a long time, about 2 - 4 hours. Once this is done, OpenCV will be installed.

### Installing OpenCV -- Mac OS X

OpenCV must be installed for this project to work. To install OpenCV's latest release, use Homebrew:

```
brew install opencv3 --with-python3 --with-tbb --with-cuda --with-contrib
```

This is a long process. After it is completed, you will have to link the python libraries. Find the generated ```cv2.so``` file, then copy it. Next, identify your local python instance's site-packages repository. Finally, copy the ```cv2.so``` file into the site-packages directory.

To test the installation, simply enter a quick command into terminal

```
python3 -c 'import cv2; print(cv2.__version__)'
```

This should print something like ```3.1.0```. If you get an error, that means that you did not install OpenCV correctly.

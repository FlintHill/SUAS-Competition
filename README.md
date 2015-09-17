# SUAS-Competition

## Status and Future Roadmap

Since the 2015 SUAS-Competition just finished, this will not be actively updated for a couple of months. However, the future roadmap, if you would like to contribute or just look at it, is below:

- Apply machine learning to recognize shapes ( ie targets )
- Apply machine learning to recognize letters

## License Information
Copyright 2015-2016 Vale Tolpegin

Licensed under the MIT License. Please see the LICENSE file for more information

## Installation

A number of dependencies must be setup before you can use this library.

### Installing OpenCV

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

## Running

To run this package, do the following ( once you are in the SUAS-Competition library ).

```
python processor.py
```

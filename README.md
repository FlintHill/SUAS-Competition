# SUAS-Competition

Flint Hill School's code for the Student Unmanned Aerial Systems competition.

## License Information
Copyright 2015-2016 Vale Tolpegin

Licensed under the MIT License. Please see the LICENSE file for more information

## Installation

First, you need to clone this repository and install it.

```
git clone https://github.com/FlintHill/SUAS-Competition.git
cd SUAS-Competition
pip install . --upgrade
```

After you have installed the code, install the dependencies.

### Installing Python

Python 2.7.x must be installed. Without it, OpenCV will not install correctly and nothing will work.

### Installing OpenCV -- Raspberry Pi

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
brew install opencv3 --with-python3
```

This is a long process. After it is completed, you will have to link the python libraries.

```
echo /usr/local/opt/opencv3/lib/python2.7/site-packages >> /usr/local/lib/python2.7/site-packages/opencv3.pth
mkdir -p /Users/{ADD YOUR USERNAME HERE}/Library/Python/2.7/lib/python/site-packages
echo 'import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")' >> /Users/{ADD YOUR USERNAME HERE}/Library/Python/2.7/lib/python/site-packages/homebrew.pth
```

To test the installation, simply enter a quick command into terminal

```
python -c 'import cv2; print(cv2.__version__)'
```

This should print something like ```3.1.0```. If you get an error, that means that you did not install OpenCV correctly.

## Installing & Setting up the Interoperability server

### Installation & Testing

To setup the server, you need to follow this documentation: http://auvsi-suas-competition-interoperability-system.readthedocs.org/en/latest/index.html#

Specifically, if you would like to reduce overhead and simplify the installation process on a VM, follow the below steps:

1. Identify & download appropriate Ubuntu operating system .iso file. Since this is subject to change, you need to look at the above documentation to find the latest
2. Clone Github repository by running the following commands

```
$ sudo apt-get -y install git
$ cd ~/
$ git clone https://github.com/auvsi-suas/interop.git
```

3. Setup the installation

```
$ cd ~/interop/setup
$ ./setup.sh
```

4. Attempt to run tests

```
$ cd ~/interop
$ ./test.sh
```

If this fails and the Python clients are the cause of the errors thrown, run the following commands. Following the completeion of these commands, restart the server and rerun the tests (commands located right above).

```
$ cd ~/interop/server
$ source venv/bin/activate
$ python manage.py loaddata fixtures/test_fixture.yaml
```

### Operation

1. Make sure your local network is configured as is requested in the manual

2. Run the Interop VM (after going through the installation process)

3. Verify the interop server is running

4. Run the local server ```python interop/clientproxy.py --url http://IP_ADDRESS_OF_INTEROP --username USERNAME --password PASSWORD```

5. Finally, run the Mission Planner script through MPI's scripting interface

### Exporting database to JSON

```
$ cd ~/interop/server
$ source venv/bin/activate
$ python manage.py dumpdata > exported.json
```

### Resetting database

```
$ cd ~/interop/server
$ source venv/bin/activate
$ python manage.py syncdb
```
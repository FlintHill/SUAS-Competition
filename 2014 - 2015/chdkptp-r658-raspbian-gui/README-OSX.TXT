chdkptp is not developed or tested on Mac, user Achim on the CHDK wiki reports following
creates a working cli-only build for for OSX 10.8. Thanks!

A user has also reported success building the GUI libraries in this post
http://chdk.setepontos.com/index.php?topic=6231.msg96753#msg96753

Comments and corrections are welcome on the chdkptp development thread:
http://chdk.setepontos.com/index.php?topic=6231.0

========

1) brew install lua libusb
2) svn co http://subversion.assembla.com/svn/chdkptp/trunk/ chdkptp
3) create config.mk
========
cp config-sample-linux.mk config.mk

change:
LUA_INCLUDE_DIR=/usr/local/opt/lua/
LUA_LIB=lua

4) Build with 'make'
5) update chdkptp-sample.sh
========

    adjust the following to your configuration 

CHDKPTP_DIR=`pwd`
export LUA_PATH="$CHDKPTP_DIR/lua/?.lua"

reyalp note: 
Above will only work if the shell script is executed from the directory with chdkptp. Use a hard code path
like /usr/local/chdkptp if you want to be able to run from anywhere.

6) Prevent PTPCamera from hogging:
sudo chmod -x "/System/Library/Image Capture/Devices/PTPCamera.app/Contents/MacOS/PTPCamera"
(more fine-grained control: https://github.com/mejedi/mac-gphoto-enabler/blob/master/gphoto-enable.sh)

7) run via ./chdkptp-sample.sh 
examples:
./chdkptp-sample.sh -h
./chdkptp-sample.sh -c 


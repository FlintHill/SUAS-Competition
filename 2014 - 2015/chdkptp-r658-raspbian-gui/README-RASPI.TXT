The raspberrypi binary includes GUI and CLI executables, named chdkptp_gui and chdkptp respectively
The GUI executable requires IUP and CD libraries which are non-trivial to build on raspberry pi
These binaries are available in a separate package called chdkptp-raspbian-libs-<date>.zip
To use the libraries with the GUI build, your chdkptp.sh should be set up to point to the chdkptp_gui
executable and add the libs to LD_LIBRARY_PATH.
Assuming you extracted the chdkptp package and the libs into a directory called /home/pi/pietest
it should look something like this

#!/bin/sh
CHDKPTP_DIR=/home/pi/pietest
export LD_LIBRARY_PATH=$CHDKPTP_DIR/cd/lib:$CHDKPTP_DIR/iup/lib
export LUA_PATH="$CHDKPTP_DIR/lua/?.lua"
"$CHDKPTP_DIR/chdkptp_gui" "$@"

The CLI build should have no external dependencies that aren't part of the standard system

Information on building the libraries can be found in README-RASPI-LIBS.TXT

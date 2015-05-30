#!/bin/sh
# copy this file to chdkptp.sh and ajust for your configuration
# to use the GUI build from a binary package that includes both CLI and GUI change to chdkptp_gui
CHDKPTP_EXE=chdkptp
# path where chdkptp is installed
CHDKPTP_DIR=/home/pi/Desktop/chdkptp-r658-raspbian-gui
# LD_LIBRARY_PATH for shared libraries
# only need if you have compiled IUP support and have NOT installed the libraries to system directories 
export LD_LIBRARY_PATH=$CHDKPTP_DIR/libs.cd:$CHDKPTP_DIR/libs/iup
export LUA_PATH="$CHDKPTP_DIR/lua/?.lua"
"$CHDKPTP_DIR/$CHDKPTP_EXE" "$@"

# ***NOTE: THIS DOCUMENT HAS BEEN MODIFIED***

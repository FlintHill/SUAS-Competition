The chdkptp raspberry pi library package provides Lua 5.1, Lua 5.2, IUP and CD
compiled for the raspbian distribution. The latest package can be found
in the chdkptp files area:
https://www.assembla.com/spaces/chdkptp/documents

Information about chdkptp can be found at:
http://www.assembla.com/wiki/show/chdkptp

For information about Lua, CD and IUP, see
http://www.lua.org/
http://www.tecgraf.puc-rio.br/iup/
http://www.tecgraf.puc-rio.br/cd/

The zip is arranged into directories for each library:
lua5.1, lua52, cd and iup respectively

See COPYRIGHT file or doc subdirectory in each directory for copyright
information.

These files are intended to allow you to run the chdkptp GUI binary on
raspberry pi, or build your own chdkptp without building the GUI libraries.
Some files not required by CHDK are included, but these are not complete
distributions of Lua, CD and IUP, and are not thoroughly tested. 

Using the libraries with chdkptp:
See README-RASPI.TXT in the chdkptp package or source.

Using the libraries to build chdkptp:
Use something like the following in your config.mk

TEC_LIBS=/path/to/zip/contents

ifeq ("$(USE_LUA_52)","1")
LUA_INCLUDE_DIR=$(TEC_LIBS)/lua52/include
LUA_LIB_DIR=$(TEC_LIBS)/lua52/lib
else
LUA_INCLUDE_DIR=$(TEC_LIBS)/lua5.1/include
LUA_LIB_DIR=$(TEC_LIBS)/lua5.1/lib
endif

# lib paths - only needed if you haven't installed in system directories
IUP_LIB_DIR=$(TEC_LIBS)/iup/lib
IUP_INCLUDE_DIR=$(TEC_LIBS)/iup/include
CD_LIB_DIR=$(TEC_LIBS)/cd/lib
CD_INCLUDE_DIR=$(TEC_LIBS)/cd/include


Build notes:
The libraries were built on 2014-01-07-wheezy-raspbian.zip
While there are a few pi specifics, the following may also be useful
building on other distros.

The build mostly follows the directions given at
http://www.tecgraf.puc-rio.br/iup/en/building.html
but several additional workarounds are required. The build was done
without using the distro provided Lua packages, and without using tecmake.

Both Lua 5.1 and Lua 5.2 are used, to simplify building the other libraries.
It is strongly recommended that you build chdkptp with Lua 5.2

The following packages should be installed
libreadline-dev
libncurses5-dev
libfreetype6-dev
libx11-dev
libxpm-dev
libxmu-dev
libxft-dev
libgtk2.0-dev
libgl1-mesa-dev
libglu1-mesa-dev
libwebkitgtk-dev

Download the source packages
$ wget http://www.lua.org/ftp/lua-5.1.5.tar.gz
$ wget http://www.lua.org/ftp/lua-5.2.3.tar.gz
$ wget http://sourceforge.net/projects/imtoolkit/files/3.8.2/Docs%20and%20Sources/im-3.8.2_Sources.tar.gz
$ wget http://sourceforge.net/projects/canvasdraw/files/5.7/Docs%20and%20Sources/cd-5.7_Sources.tar.gz
$ wget http://sourceforge.net/projects/iup/files/3.10.1/Docs%20and%20Sources/iup-3.10.1_Sources.tar.gz

$ tar -xzf lua-5.1.5.tar.gz

$ tar -xzf lua-5.2.3.tar.gz

$ tar -xzf im-3.8.2_Sources.tar.gz
$ tar -xzf cd-5.7_Sources.tar.gz
$ tar -xzf iup-3.10.1_Sources.tar.gz

The IM, CD and IUP tar files did not have execute permissions on the directories.
This can be fixed with the following:

$ find im cd iup -type d -exec chmod a+x {} \;

The default tekmake.mak files do not properly detect the raspbian as arm,
which in turn makes it define TEC_BIGENDIAN. Apply the included
tecmake.mak.patch patch with

$ for d in im cd iup ; do pushd $d ; patch -p0 <../tecmake.mak.patch ; popd ; done

Build Lua
cd lua-5.1.5
make linux
make INSTALL_TOP=/home/pi/teclibs/lua5.1 install

cd lua-5.2.3
make linux
make INSTALL_TOP=/home/pi/teclibs/lua52 install

The different naming conventions above are intentional, to conform to the
pattern expected by the other libraries.

The IUP build expects a different sub-path than the above install creates.
Use the following to put symlinks in the required location

$ mkdir lua5.1/lib/Linux310
$ ln -s ../liblua.a lua5.1/lib/Linux310/liblua5.1.a
$ mkdir lua52/lib/Linux310
$ ln -s ../liblua.a lua52/lib/Linux310/liblua52.a

Several includes are not found correctly in the IUP and CD build processes.
Set the following before building. This is probably distro specific, adjust
if you continue to get include errors.

$ export CPATH=/usr/include/gtk-unix-print-2.0:/usr/include/webkitgtk-1.0:/usr/include/libsoup-2.4:/usr/lib/arm-linux-gnueabihf/glib-2.0/include

Build IM (not directly required by chdkptp, but required by the other libs)

$ cd im && make

Build CD

$ cd cd && make USE_PKGCONFIG=Yes

Build additional CD components required for "context plus" (optional)

$ cd cd/src && make USE_PKGCONFIG=Yes cdx11 cdcontextplus cdluacontextplus5 cdcairo

Build IUP

cd iup && make USE_PKGCONFIG=Yes

The default CD and IUP builds make a lot of libraries that are not currently
required by chdkptp. It might be better to just build the required libraries
individually.

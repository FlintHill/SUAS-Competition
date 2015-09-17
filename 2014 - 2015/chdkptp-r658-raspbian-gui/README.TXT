=Introduction=
chdkptp is a tool to access the custom PTP extension of the CHDK firmware addon for canon
cameras. 

This is an alpha version - protocol, functionality, APIs, commands, command line options 
are all subject to change.

Source is available from http://subversion.assembla.com/svn/chdkptp/
Binary snapshot builds are available from http://www.assembla.com/spaces/chdkptp/documents
Roadmap is under development in http://www.assembla.com/spaces/chdkptp/tickets
Changelog is at http://www.assembla.com/wiki/show/chdkptp/Changelog

This README is primarily intended for developers.

Documentation for end users can be found in USAGE.TXT

Installation information can be found in INSTALL.TXT

Information about the Raspberry pi binary builds can be found in README-RASPI.TXT

For information about CHDK, see http://chdk.wikia.com/wiki/CHDK
For information about the CHDK PTP extension, see http://chdk.wikia.com/wiki/PTP_Extension

chdkptp is forked from libptp and ptpcam, as modified by mweerden, the chdkde project developers
and others. All source is released under GPL or MIT licenses

The original ptpcam source, written by Mariusz Woloszyn < emsi[A@T]ipartners.pl >
is available from http://libptp.sourceforge.net/

mweerdens modified version can be found at https://github.com/mweerden/CHDK/tree/ptp

the CHDKDE ptpcam source may be found at http://tools.assembla.com/chdkde/browser/trunk/tools/ptpcam

chdkptp includes software from several other projects, see THANKS.TXT for details.

=Dependencies=
- IUP version 3.10.1 http://www.tecgraf.puc-rio.br/iup/ (earlier 3.x versions may also work)
  Optional, edit config.mk to build without IUP GUI support
- CD Version 5.7 http://www.tecgraf.puc-rio.br/cd/ (earlier 5.x versions may also work)
  Optional, used for remote display
- Lua version 5.2 http://www.lua.org/
  chdkptp no longer supports Lua 5.1, although it may work
- LibUSB (libusb-win32 on windows)
- GNU readline
  Optional, recommended on Linux

=Windows development environment=
Mingw with gcc 4.8+ is the primary development environment. 
All instructions below assume you are using this.
Using a mingw bash shell for development is suggested.

==Installing mingw==
http://www.mingw.org/
Download the gui installer. Install at least mingw C compiler.
C++ support is required to use CD "context plus", not required or used by default.
Msys is suggested, and may be required

==Installing IUP libraries==
Get the mingw4 binary package of IUP, 
http://sourceforge.net/projects/iup/files/

Note, this package has the libraries in the root, with etc/ and include/ subdirectories.
You may want to put the libraries in /lib to match the IUP recommended filesystem layout
The examples and win32 binaries are not required, but may be helpful

==Installing CD libraries==
Similar to IUP, from http://sourceforge.net/projects/canvasdraw/files/

==Installing and building Lua==
Get the lua 5.2.x source from http://www.lua.org/download.html
In a msys shell, go to the lua directory and type
make mingw
make local

NOTE:
it's very important that Lua be linked to exactly the same C runtime library
as chdkptp itself. The lbuf file routines expect to be able to fread and fwrite on
a FILE * opened by lua io.open()

This condition probably won't be met if you use a pre-compiled Lua dll on windows.
It's probably OK with a shared lua in typical linux environments. 
If in doubt, build your own Lua with the same compiler you build chdkptp with.

==Installing LibUSB development package==
TODO
describe filter driver installation
http://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.4.0/
libusb-win32-bin-1.2.4.0.zip
Unzip somewhere convenient

Some earlier and later versions will also probably work

=Linux development environment=
The following is based on Ubuntu 10.04, 64 bit. YMMV
Install the following packages and any required dependencies 
libusb-1.0-0
libusb-dev (may be called libusb-1.0-dev ?)

Lua
Packages will be called something like
liblua5.2-dev
liblua5.2

Alternately, you may download and build your own. This is suggested
if you are building IUP and CD from source.

GNU readline 
You need the development package, probably called something like 
libreadline6-dev or something like that

IUP - using precompiled binaries
Download the appropriate IUP library for your platform from 
http://www.tecgraf.puc-rio.br/iup/
unpack the package
adjust the IUP_LIB_DIR and IUP_INCLUDE_DIR in config.mk
You will also need a fully working gcc environment.

CD - similar to IUP

==Building IUP and CD==
If available, using pre-compiled libraries is suggested, but if you want to
build from source some notes can be found in README-RASPI-LIBS.TXT

=Configuring the source (all platforms)=
Edit config.mk to reflect the installation directories of the above packages and
desired compile time options
See config-sample-*.mk for examples

==Mac development==
See README-OSX.TXT

=Building=
make

On windows, link occasionally fails with something like
 /mingw/bin/../lib/gcc/mingw32/4.8.1/../../../../mingw32/bin/ld.exe: reopening chdkptp.exe: Permission denied

Rebuilding seems to work around the problem

=Testing your build=
To test some internal functions use
chdkptp -e"exec require'tests':runall()"
note, this should be run from the same directory as the CHDKPTP executable

This will create (or overwrite) a file called lbuftest.dat in the current
directory, and delete it when the test completes.

To test functions that connect to the camera, use
chdkptp -e"exec require'camtests'.runbatch{bench=true,filexfer=true}"

If more than one camera is connected to the system, a random one will be used
unless you also specify devspec={dev="device name",bus="bus id"}

The filexfer tests will create and delete a local directory called camtests
in the current working directory. If you already have a directory of this name,
it will be deleted when the test completes.

Camtests will also create and delete some files and directories on the camera.

The final line of output from both test modules should be 
failed 0

For for vesions prior to r562, camtests shoud be invoked with
chdkptp -e"exec require'camtests'.runstd()"

None of the above is a comprehensive test of chdkptp functionality.

=Running=
See USAGE.TXT

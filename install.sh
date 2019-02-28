#!/bin/bash
"""
run this file to install the necessary Dependencies to run the code. 
"""


git clone https://github.com/auvsi-suas/interop
cd interop/client
cd auvsi_suas
mkdir proto
cp ../../proto/*.* proto/
cd ..
sudo -H python -m pip install -r requirements.txt
sudo -H python -m pip install . -U
cd ../../
sudo rm -r interop

git clone https://github.com/FlintHill/simple-websocket-server
cd simple-websocket-server
sudo -H python -m pip install . -U
cd ../
sudo rm -r simple-websocket-server

sudo -H python -m pip install -U -r requirements.txt

#!/bin/bash

git clone https://github.com/auvsi-suas/interop
cd interop/client
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


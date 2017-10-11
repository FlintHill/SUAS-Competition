#!/bin/bash

git clone https://github.com/auvsi-suas/interop
cd interop/client
pip install -r requirements.txt
pip install . -U
cd ../../

git clone https://github.com/FlintHill/simple-websocket-server
cd simple-websocket-server
pip install . -U
cd ../

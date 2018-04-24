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

<<<<<<< HEAD
sudo -H python -m pip install dronekit
sudo -H python -m pip install wxpython

sudo -H python -m pip install ./SyntheticDataset -U
sudo -H python -m pip install ./UpdatedSyntheticDataset -U
sudo -H python -m pip install ./EigenFit -U
sudo -H python -m pip install ./ImgProcessingCLI -U
sudo -H python -m pip install ./SUASSystem -U
sudo -H python -m pip install ./SDAPackage -U
sudo -H python -m pip install ./SDAPackageWithVectorField -U
sudo -H python -m pip install ./VectorFieldSDASimulatorPackage -U
=======
sudo -H python -m pip install -U -r requirements.txt
>>>>>>> c5f9b7300e45fa16736418a6de168a26b34f1812

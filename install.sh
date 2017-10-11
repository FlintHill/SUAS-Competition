#!/bin/bash

sh ./install_external.sh

sudo -H python -m pip install dronekit

sudo -H python -m pip install ./SyntheticDataset -U
sudo -H python -m pip install ./EigenFit -U
sudo -H python -m pip install ./ImgProcessingCLI -U
sudo -H python -m pip install ./SUASSystem -U
sudo -H python -m pip install ./SDAPackage -U

# Update all packages

git clone https://github.com/auvsi-suas/interop
cd interop/client
sudo -H python -m pip install -r requirements.txt
sudo -H python -m pip install . -U
cd ../../
sudo rm -r interop

sudo -H python -m pip install ./EigenFit -U
sudo -H python -m pip install ./ImgProcessingCLI -U
sudo -H python -m pip install ./SUASSystem -U
sudo -H python -m pip install ./SDAPackage -U

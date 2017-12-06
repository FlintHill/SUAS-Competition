# setup ubuntu
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y

# get apps
sudo apt install git -y

# get pip
cd ~/Downloads/
sudo apt install -y python3-pip

#install Flask
sudo -H pip3 install flask
# install gphoto
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh

# move service file
cd /home/odroid/Desktop/SUAS-Competition/scripts/gcs/a6000
cp a6000.service /etc/systemd/system/a6000.service

# enable service
systemctl enable a6000

# ask for restart to test if service boots up correctly
echo "Finished installation"

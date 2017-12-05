# setup ubuntu
apt-get update
apt-get upgrade -y
apt-get dist-upgrade -y

# get apps
apt-get install git -y

# get pip
cd ~/Downloads/
sudo apt-get install python-pip

#install Flask
sudo pip install flask
# install gphoto
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh

# move service file
cd /home/odroid/Desktop/SUAS-Competition/scripts/gcs/a6000
cp a6000.service /etc/systemd/system/a6000.service

# enable service
systemctl enable a6000
systemctl status a6000

# ask for restart to test if service boots up correctly
echo "Finished installation. Restarting in 10 seconds..."
sleep 10
sudo reboot now

# setup ubuntu
apt-get update
apt-get upgrade -y
apt-get dist-upgrade -y

apt-get update
apt-get upgrade -y
apt-get dist-upgrade -y

# get apps
apt-get install git -y

# get pip
cd ~/Downloads/

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py

# install gphoto
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh

# create service file
touch a6000.service

echo "[Unit]" >> a6000.service
echo "Description=A6000 Camera Picture Take and Serve" >> a6000.service
echo "" >> a6000.service
echo "[Service]" >> a6000.service
echo "ExecStart=/home/$USER/Desktop/SUAS-Competition/scripts/gcs/a6000/startup_picture_serve_and_take.sh" >> a6000.service
echo "User=odroid" >> a6000.service
echo "Group=root" >> a6000.service
echo "StandardOutput=null" >> a6000.service
echo "" >> a6000.service
echo "[Install]" >> a6000.service
echo "WantedBy=multi-user.target" >> a6000.service
echo "" >> a6000.service

mv a6000.service /etc/systemd/system/a6000.service

# enable service
systemctl enable a6000
systemctl status a6000

# ask for restart to test if service boots up correctly
echo "Finished installation. Restarting in 10 seconds..."
sleep 10
sudo reboot now

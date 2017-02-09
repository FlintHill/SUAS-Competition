# Image Processing Scripts

This folder contains the scripts required to run image processing on a device.

To install the startup script, run the following commands on the tk1:
```
sudo cp /path/to/startup_script.sh /etc/init.d/startup_script.sh
chmod +x /etc/init.d/startup_script.sh
sudo update-rc.d startup_script.sh defaults
```

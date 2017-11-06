#!/bin/sh

cd /home/pi/Desktop/SUAS-Competition/scripts/gcs/a6000_camera_management/

python picture_Serve.py &
sleep 10
bash picture_taker.sh &

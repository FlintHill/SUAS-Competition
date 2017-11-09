#!/bin/sh -

A6000_PATH=/home/odroid/Desktop/SUAS-Competition/scripts/gcs/a6000

cd /home/odroid/Desktop/SUAS-Competition/scripts/gcs/a6000

python $A6000_PATH/picture_server.py &
sleep 10
bash $A6000_PATH/picture_taker.sh

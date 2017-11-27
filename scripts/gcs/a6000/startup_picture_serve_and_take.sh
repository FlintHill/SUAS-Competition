#!/bin/bash

cd /home/odroid/Desktop/SUAS-Competition/scripts/gcs/a6000

python picture_server.py &
sleep 10
bash picture_taker.sh

#!/bin/bash

fn=$(date +%s)

while [ true ]
do
  gphoto2 --capture-image-and-download --filename image-$fn
  /home/pi/Desktop/sendpictures.sh

  sleep 5
done

#!/bin/bash

WAIT_TIME=5

mkdir imgs
cd imgs

while [ true ]
do
  fn=$(date +%s)
  gphoto2 --capture-image-and-download --filename image-$fn.jpg

  sleep $WAIT_TIME
done

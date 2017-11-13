#!/bin/bash

waitTime = 5

while [ true ]
do
  fn=$(date +%s)
  gphoto2 --capture-image-and-download --filename image-$fn.jpg
  mv image-$fn.jpg imgs/
  sleep $waitTime
done

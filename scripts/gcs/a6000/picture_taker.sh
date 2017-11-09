#!/bin/bash

while [ true ]
do
  fn=$(date +%s)
  gphoto2 --capture-image-and-download --filename image-$fn.jpg
  mv image-$fn.jpg imgs/
  sleep 5
done

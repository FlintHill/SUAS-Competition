#!/bin/bash

fn=$(date +%s)

while [ true ]
do
  gphoto2 --capture-image-and-download --filename image-$fn.jpg
  mc image-$fn.jpg imgs/
  sleep 5
done

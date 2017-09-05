#!/usr/bin/python

# imports sorted in order of use
import os
import math
import requests
import sys
from time import sleep

"""
  CREATED BY AND FOR FLINTHILL AUVSI SUAS TEAM ||| v0.3
    [Educational Purposes]

  NOTES:
    Zoom levels range from 0-19 on main OSM server.

    URL path looks like: http://a.tile.openstreetmap.org/{zoom/z}/{longitude/x}/{latitude/y}.png
      Latitude runs horizontally to north and south poles.
      Longitude runs vertically.

    deg2num() and num2deg() comes straight from wiki:
      http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
"""

# convert from degrees to numbers
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

# convert from numbers to degrees
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def inRange(val, zoom):
  #print("val of " + str(val) + " is >= 0 and val of " + str(val) + " <= ((2**" + str(zoom) + " - 1))")
  return (val >= 0 and val <= ((2**zoom) - 1))

# downloads a file from a specific url
def download_file(url, filepath):
  print("")
  print("Downloading " + url)

  checkDirectory(filepath)

  local_filename = url.split('/')[-1]
  # NOTE the stream=True parameter
  r = requests.get(url, stream=True)
  with open(filepath + local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024): 
      if chunk: # filter out keep-alive new chunks
        f.write(chunk)
        #f.flush() commented by recommendation from J.F.Sebastian
  return local_filename

# checks if a directory exists, if not, then adds it
def checkDirectory(dir, clip=False):
  if not os.path.exists(dir):
    print("DIR_MISSING: Directory '" + dir + "' does not exist, creating...")
    os.makedirs(dir)
  else:
    print("DIR_PRESENT: Directory '" + dir + "' exists.")

print("OSM Tile Downloader v0.1")
print("========================")
#user_latitude  = input("LATITUDE:  ") # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#user_longitude = input("LONGITUDE: ") 
user_latitude = 38.14923628783763 # 38.8702
user_longitude = -76.43238529543882 # -77.3157
zoom_start = input("ZOOM START:    ")
print ("-> SERVER LETTERS ARE: 'a', 'b', and 'c'")
server = raw_input("SERVER LETTER: ")
print("")

point = deg2num(38.8702, -77.3157, 5) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

print("Center tile is... x=" + str(point[0]) + " y=" + str(point[1]) + " @ z=5")
print("")

print("Checking if zoom level directories exist...")

zooms = range(0, 20) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

for zoom in zooms:
  dir = "tile/" + str(zoom)

  if not os.path.exists(dir):
    print("DIR_MISSING: Directory '" + dir + "' for zoom or z does not exist, creating...")
    os.makedirs(dir)
  else:
    print("DIR_PRESENT: Directory '" + dir + "' exists.")
print("")

print("Directory check done.")
print("")
print("Checking if OSM site is up...")
print("")

root = "http://" + server + ".tile.openstreetmap.org/"
print("SERVER CHOSEN: " + root)

print("Contacting root: " + root + "...")

r = requests.get(root, timeout=4)

if r.status_code > 399: # 400s are client-side errors, 500s are server-side
  print("HTTP_FAILURE: Server return status code: " + str(r.status_code) + ", try again later.")
  sys.exit("---see above error: line 94")
else:
  print("HTTP_SUCCESS: Server returned status code: " + str(r.status_code))

print("")
print("")
print("!!! ALL SYSTEMS GO !!!")
print("Starting download loop...")
print("")

phase  = zoom_start
extend = 1 # int(zoom_start**1.0) + 1
count  = 0

print(" !!! PHASE IS " + str(phase))

for phase in reversed(range(0, phase)):
  extend = int(phase**1.2) + 1
  print("===> STARTING PHASE [" + str(phase) + "] OF [19]")

  calc = 0

  if phase == 0:
    calc = 1
  else:
    calc = 8*phase

  print("===>===> Tiles to download this round: " + str(calc))
  point = deg2num(float(user_latitude), float(user_longitude), phase)

  # rows and columns, go from topmost row leftmost column towards right, advance into next column 
  i = 0 # point[0] - extend
  k = 0 # point[1] - extend

  for i in range(0, (extend*2) + 1): # range(point[0] - extend, point[0] + extend + 1):
    print("### i=" + str(i))

    if inRange(point[0] - extend + i, phase) is False:
      print("Point i: " + str(i) + " is OUT OF RANGE for zoom: " + str(zoom_start) + " at EXTEND: " + str(extend))
      i += 1
      sleep(0.01)
      continue

    for k in range(0, (extend*2) + 1): # range(point[1] - extend, point[1] + extend + 1):
      x = point[0] - extend + i
      y = point[1] - extend + k

      if inRange(point[1] - extend + k, phase) is False:
        print("Point i: " + str(k) + " is OUT OF RANGE for zoom: " + str(zoom_start))
        k += 1
        sleep(0.01)
        continue

      url = str(phase) + "/" + str(x) + "/" + str(y) + ".png"
      path = str(phase) + "/" + str(x) + "/"

      if os.path.isfile("tile/" + url):
        print("'tile/" + url + "' already exists, SKIPPING...")
        continue
      else:
        print("'tile/" + url + "' does not exist, DOWNLOADING...")

      try:
        download_file(root + url, "tile/" + path)
      except ValueError:
        print("???")
      else:
        print(" ### FAILED, FILE ALREADY DOWNLOADED ### ")

      count += 1
      print("Downloaded image #" + str(count) + " within EXTEND: " + str(extend) + " and ZOOM: " + str(phase))

      print("IMAGE EXISTS AT LAT, LONG: " + str(num2deg(x, y, phase)))

      k += 1

      print("Sleep half of a second...")
      sleep(0.5)
    print("")
    print("Moving to next row...")

    i += 1
  else:
    print("Finished phase #" + str(phase))

  phase -= 1
  extend -= extend*2 + 1
  print("")

print("!!! FINISHED DOWNLOADING !!!")
print("===>===> " + str(count) + " images were downloaded")

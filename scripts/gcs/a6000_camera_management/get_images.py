from pysony import SonyAPI, payload_header
import urllib2
import thread
import time
import shutil
import os

class ClassName(object):

    def run(self):
        camera = SonyAPI()
        if options.debug:
            print "searching for camera"

        search = ControlPoint()
        cameras =  search.discover(1)

        if len(cameras):
            camera = SonyAPI(QX_ADDR=cameras[0])
        else:
            print "No camera found, aborting"
            return

        while true :
            picture_url = camera.actTakePicture()
            sleep(5)

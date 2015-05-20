__author__ = 'Vale Tolpegin'

import os
from download_image import download_image
from subprocess import *

class shoot_image:

    def __init__( self, *args, **kwargs ):
        pass

    def shoot_an_image( self ):
        #popen terminal command
        running = Popen( ['ptpcam', '--chdk="lua', "require('lptpgui').exec_luafile([[A/CHDK/SCRIPTS/$myScript]])", '"'], stdout=PIPE, stderr=PIPE, shell=True )

        #get output
        stdout, stderr = running.communicate()

        #if shot was successfully taken:
        if not stderr:
            #download image
            download = download_image()
            download.download_most_recent_image()

            return True
        else:
            return False

if __name__ == '__main__':
    test = shoot_image()

    test.shoot_an_image()
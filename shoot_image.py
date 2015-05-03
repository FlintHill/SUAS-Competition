__author__ = 'Vale Tolpegin'

import os
import download_image from download_image
import subprocess

class shoot_image:

    def __init__( self, *args, **kwargs ):
        pass

    def shoot_an_image():
        #popen terminal command
        running = Popen( ['ptpcam', '--chdk="lua', "require('lptpgui').exec_luafile([[A/CHDK/SCRIPTS/$myScript]])" + '"'], stdout=PIPE, stderr=PIPE )

        #get output
        stdout, stderr = running.communicate()

        #if shot was successfully taken:
        if not stderr:
            #download image

            return True
        else
            return False
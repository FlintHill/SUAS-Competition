__author__ = 'Vale Tolpegin'

import os
import download_image
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
            download = download_image()
            download.download_most_recent_image()

            return True
        else:
            return False

if __name__ == '__main__':
    pass
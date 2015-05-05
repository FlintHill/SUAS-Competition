__author__ = 'Vale Tolpegin'

import os
import subprocess

class download_image:

    def __init__( self, *args, **kwargs ):
        pass

    def download_most_recent_image():
        #run perl script to download most recent image
        running = Popen( [ 'pl download_images.pl' ], stdout=PIPE, stderr=PIPE )

        stdout, stderr = running.communicate()
    
        #if download was successful
        if not stderr:
            return true
        else:
            return false

if __name__ == '__main__':
    pass
__author__ = 'Vale Tolpegin'

import os
from subprocess import *

class download_image:

    def __init__( self, *args, **kwargs ):
        pass

    def download_most_recent_image( self ):
        #run perl script to download most recent image
        running = Popen( [ 'perl download_images.pl' ], stdout=PIPE, stderr=PIPE, shell=True )

        stdout, stderr = running.communicate()
    
        #if download was successful
        if not stderr:
            return True
        else:
            return False

if __name__ == '__main__':
    pass
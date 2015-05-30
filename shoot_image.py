__author__ = 'Vale Tolpegin'

import os
from subprocess import *

class shoot_image:

    def __init__( self, *args, **kwargs ):
        pass

    def shoot_an_image( self ):
        #popen terminal command
        running = Popen( [ 'cd chdkptp-r658-raspbian-gui/; bash chdkptp-sample.sh' ], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True )
        
        #Taking a picture
        running.stdin.write( 'connect\n' )
        running.stdin.write( 'rec\n' )
        running.stdin.write( 'remoteshoot ../\n' )
        running.stdin.write( 'quit\n' )

        #get output
        stdout, stderr = running.communicate()

        #if the shot was successfully taken and downloaded:
        if not stderr:
            return True
        else:
            return False

if __name__ == '__main__':
    test = shoot_image()

    test.shoot_an_image()
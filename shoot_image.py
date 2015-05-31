__author__ = 'Vale Tolpegin'

import os
from subprocess import *

class shoot_image:
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def __init__( self, *args, **kwargs ):
        pass

    def shoot_image( self ):
        #popen terminal command
        running = Popen( [ 'cd chdkptp-r658-raspbian-gui/; bash chdkptp-sample.sh' ], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True )
        
        #Taking a picture
        running.stdin.write( 'connect\n' )
        running.stdin.write( 'rec\n' )
        running.stdin.write( 'remoteshoot ../images\n' )
        running.stdin.write( 'disconnect\n' )
        running.stdin.write( 'quit\n' )

        #get output
        stdout, stderr = running.communicate()

        #if the shot was successfully taken and downloaded:
        if not stderr or "already in rec" in stderr:
            print self.bcolors.OKGREEN + "[ Info ]" + self.bcolors.ENDC + " Image Taken and Downloaded"
        else:
            print self.bcolors.FAIL + "[ Error ]" + self.bcolors.ENDC + " Encountered An Error While Taking A Picture"
            print stderr

        return True

if __name__ == '__main__':
    test = shoot_image()

    test.shoot_an_image()
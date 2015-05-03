__author__ = 'Vale Tolpegin'

import os

class clear_directory:

    def __init__( self, *args, **kwargs ):
        pass

    def empty_directory( directory_name, file_name ):
        #set output from os.walk function to appropriate variables

        #for filename in filenames found in directory walked:
        for root, dirs, files in os.walk( directory_name ):
            for filename in files:
                #if filename contains file_name:
                if file_name in filename:
                    #delete filename
                    dirs.remove( file_name )
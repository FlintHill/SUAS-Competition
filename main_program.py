__author__ = 'Vale Tolpegin'

#import all of my classes
from shoot_image import shoot_image
from image_parsing import image_parser
from clear_unwanted_files import clear_directory
from download_image import download_image

#import all remaining classes that are needed
import os
import multiprocessing

class main_program:
    #defining class objects
    global image_shooter
    global imagery_parsing
    global unwanted_file_clearer
    global image_downloader

    def __init__( self, *args, **kwargs ):
        #getting global variables
        global image_shooter
        global imagery_parsing
        global unwanted_file_clearer
        global image_downloader
        
        #instantiating global objects
        image_shooter = shoot_image()
        imagery_parsing = image_parser()
        unwanted_file_clearer = clear_directory()
        image_downloader = download_image()

    def run( self ):
        while True:
            #if incoming signal from GPIO pins
                #start a new thread with the image method
            pass

    def image_processor( self ):
        #shoot image

        #download image

        #parse image

        #if parsed image is true ( if target found )
            #save cropped image
            #save full image
        #else
            #move image to trash directory
        pass

if __name__ == 'main':
    #create new object of the main program class
    current_main = main_program()

    #run the program
    current_main.run()
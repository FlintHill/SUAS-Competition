__author__ = 'Vale Tolpegin'

#import all of my classes
import shoot_image from shoot_image
import image_parser from image_parser
import clear_unwanted_files from clear_unwanted_files
import download_image from download_image

#import all remaining classes that are needed
import os
import runnable

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
        unwanted_file_clearer = clear_unwanted_files()
        image_downloader = download_image()

    def run( self ):
        while True:
            #if incoming signal from GPIO pins
                #start a new thread with the image method

    def image_processor( self ):
        #shoot image

        #download image

        #parse image

        #if parsed image is true ( if target found )
            #save cropped image
            #save full image
        #else
            #move image to trash directory

if __name__ == 'main':
    #create new object of the main program class
    current_main = main_program()

    #run the program
    current_main.run()
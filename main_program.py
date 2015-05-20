__author__ = 'Vale Tolpegin'

#import all of my classes
from shoot_image import shoot_image
from image_parsing import image_parser
from clear_unwanted_files import clear_directory
from download_image import download_image
from gpio_shooting import gpio_shooting

#import all remaining classes that are needed
import os
import multiprocessing

class main_program:
    #defining class objects
    global image_shooter
    global imagery_parsing
    global unwanted_file_clearer
    global image_downloader
    global gpio_shooter

    def __init__( self, *args, **kwargs ):
        #getting global variables
        global image_shooter
        global imagery_parsing
        global unwanted_file_clearer
        global image_downloader
        global gpio_shooter
        
        #instantiating global objects
        image_shooter = shoot_image()
        imagery_parsing = image_parser()
        unwanted_file_clearer = clear_directory()
        image_downloader = download_image()
        gpio_shooter = download_image() #gpio_shooting()
    
        #initiating all objects that have to be initiated
        #NOTE: THE ARGUEMENT NEEDS TO BE UPDATED WITH THE FINAL ARGUEMENT
        gpio_shooter.setup_gpio_pin( 10 )

    def run( self ):
        global gpio_shooter
        
        while True:
            #if incoming signal from GPIO pins
            if gpio_shooter.get_shot_truefalse():
                #start a new thread with the image method
                multiprocessing.Process(target=self.image_processor, args=()).start()

    def image_processor( self ):
        global image_shooter
        global image_downloader
        global image_parsing
        
        #shoot image
        image_shooter.shoot_image()

        #download image
        name = image_downloader.download_most_recent_image()
        
        if name != False:
            #parse image & set image test variable to true if successful
            target = image_parsing.process_img()

if __name__ == 'main':
    #create new object of the main program class
    current_main = main_program()

    #run the program
    current_main.run()
__author__ = 'Vale Tolpegin'

#import all of my classes
from shoot_image import shoot_image
from image_parsing import image_parser
#from gpio_shooting import gpio_shooting

#import all remaining classes that are needed
import os
import multiprocessing
import time

class main_program:
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    
    #defining class objects
    global image_shooter
    global imagery_parsing
    global gpio_shooter

    def __init__( self, *args, **kwargs ):
        #getting global variables
        global image_shooter
        global imagery_parsing
        #global gpio_shooter
        
        #instantiating global objects
        image_shooter = shoot_image()
        imagery_parsing = image_parser()
        #gpio_shooter = gpio_shooting()
    
        #initiating all objects that have to be initiated
        #NOTE: THE ARGUEMENT NEEDS TO BE UPDATED WITH THE FINAL PIN NUMBER
        #gpio_shooter.setup_gpio_pin( 10 )

    def run( self ):
        #global gpio_shooter
        
        multiprocessing.Process(target=self.get_images, args=()).start()
        
        while True:
            print self.bcolors.OKGREEN + "[ Info ]" + self.bcolors.ENDC + " Image Finding Started"
                
            self.image_processor()

    def get_images( self ):
        #getting global variables
        global image_shooter
        
        while True:
            #shoot image
            if True: #gpio_shooter.shoot_truefalse():
                image_shooter.shoot_image()
                
            time.sleep( 20 )


    def image_processor( self ):
        #getting global variables
        global imagery_parsing
        
        #setting the image filename to nothing
        file_name = ""
        
        #getting images that need to be processed
        for root, dirs, files in os.walk( os.getcwd() + "/images/" ):
            #for every file in the directory
            for file in files:
                #if the file is an image
                if ".jpg" in file:
                    #and the image is not metadata left after the image has been moved/deleted
                    if file[0] == ".":
                        #skip the image
                        pass
                    else:
                        #otherwise, if the image is a real image that needs to be parsed
                        print self.bcolors.OKGREEN + "[ Info ]" + self.bcolors.ENDC + " Image found"
                        file_name = file

                        #stop looking at additional files since an image has already been found
                        break

        #if an image was not found in the images directory, return after 5 seconds
        if file_name == "":
            #print no images found in directory
            print self.bcolors.WARNING + "[ Warning ]" + self.bcolors.ENDC + " No Images Found In Images Directory "
            
            #wait 5 seconds
            time.sleep( 5 )
            
            #return, where this method will be called again
            return
        
        #parse image & if successful, move image to positive images folder
        print self.bcolors.OKGREEN  + "[ Info ]" + self.bcolors.ENDC + " Parsing Image"
        if imagery_parsing.process_img( "images/" + file_name ):
            os.rename( "../images/" + file_name, "../positive_images/" + file_name )
            os.unlink( os.getcwd() + "/images/" + file_name )
            print self.bcolors.OKGREEN + "[ Info ]" + self.bcolors.ENDC + " Image Copied Over To Positive Images Folder"
        #otherwise, if the parsing is not successful, move the file to the negative images folders
        else:
            os.rename( "../images/" + file_name, "../negative_images/" + file_name )
            os.unlink( os.getcwd() + "/images/" + file_name )
            print self.bcolors.OKGREEN + "[ Info ]" + self.bcolors.ENDC + " Image Copied Over To Negative Images Folder"


if __name__ == '__main__':
    #create new object of the main program class
    current_main = main_program()

    #run the program
    current_main.run()
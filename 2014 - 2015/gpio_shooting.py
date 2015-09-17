__author__ = 'Vale Tolpegin'

import RPi.GPIO as GPIO

#setting default GPIO board settings
GPIO.setmode( GPIO.BOARD )

class gpio_shooting:
    #Rx pin
    inPin = 0

    def __init__( self, *args, **kwargs ):
        pass
    
    def setup_gpio_pin( self, rx ):
        global inPin
        
        try:
            #start a gpio connection with Rx pin
            GPIO.setup( rx, GPIO.IN )
        except:
            print "[ Error ] Could not setup GPIO pin. Please restart program"
        
        inPin = rx

    def get_shot_truefalse( self ):
        global inPin
        
        if GPIO.input( inPin ):
            return true
        else:
            return false

if __name__ == '__main__':
    pass
__author__ = 'Vale'

import numpy as np
import datetime
import cv2

class image_parser:
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    # These are1 the global image settings. These are set by specifically referencing them through the parser's properties
    global PIXEL_COLOR_THRESHOLD
    global LOWER_CONTOUR_AREA
    global HIGHER_CONTOUR_AREA
    global BLACK_COLOR_THRESHOLD
    global ADJACENT_OBJECT_INDEX

    # This method is the initialization method and sets all of the picture settings to default
    def __init__( self, *args, **kwargs ):
        #getting global variables
        global PIXEL_COLOR_THRESHOLD
        global LOWER_CONTOUR_AREA
        global HIGHER_CONTOUR_AREA
        global BLACK_COLOR_THRESHOLD
        global ADJACENT_OBJECT_INDEX

        #setting global variables' values
        PIXEL_COLOR_THRESHOLD = 0
        BLACK_COLOR_THRESHOLD = 5
        LOWER_CONTOUR_AREA = 1200
        HIGHER_CONTOUR_AREA = 100000
        ADJACENT_OBJECT_INDEX = 0

    # This method is called when the user would like to process any given image. This method completes the following in the image processing process:
    # 1: Find objects in the passed image
    # 2: For each object, as long as they fit a size parameter, parse/process that object to see if it fits a target's characteristics
    # 3: If the object fits a target's characteristics, save that image to a particular directory
    def process_img( self, img_name ):
        #get global variables
        global LOWER_CONTOUR_AREA
        global HIGHER_CONTOUR_AREA

        #get current time; this allows me to time the total length of the processing
        start_time = datetime.datetime.now()

        #reading in image
        img = cv2.imread( img_name )
        img_viewing = cv2.imread( img_name )

        try:
            hsv = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )
            grey = cv2.cvtColor( hsv, cv2.COLOR_BGR2GRAY )
        except:
            print self.bcolors.FAIL + "[ Error ]" + self.bcolors.ENDC + " Failed Image Parsing"
            print self.bcolors.OKBLUE + "[ Action ]" + self.bcolors.ENDC + " Resetting Thread"
            return ""

        #finding the objects in the image
        ret,thresh = cv2.threshold(grey,127,255,0)
        contours,h = cv2.findContours(thresh,1,2)

        #for each contour
        for cnt in contours:
            #creating temporary variable to hold the non-translated contours
            object_coordinates = np.array( cnt, dtype=np.int32 )

            #if the object is either too small or too large, skip parsing
            if cv2.contourArea(cnt) < LOWER_CONTOUR_AREA or cv2.contourArea( cnt ) > HIGHER_CONTOUR_AREA:
                pass
            #otherwise, parse object
            else:
                object_bool = self.crop_img( cnt, img )

                if object_bool:
                    cv2.drawContours(img_viewing, contours, -1, (255,0,0), 3)

                    print self.bcolors.OKGREEN + "[ Info ]" + self.bcolors.ENDC + " Finished processing " + img_name[7:] + " at " + str(datetime.datetime.now())
                    #return "True"

        cv2.imshow( "img_viewing", img_viewing )
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #print the total time it took to parse the image
        print self.bcolors.OKGREEN + "[ Info ]" + self.bcolors.ENDC + " Finished processing " + img_name + " at " + str(datetime.datetime.now())
        return "False"

    # Main image processing method. This method will do the following things:
    # 1: Crop the image. This will create the smallest ( almost, with some border ) bounding rectangle around the object in question
    # 2: Find the largest object in the cropped image. Since the cropped image is the bounding rect of the object in question, that object will be the largest object in the image using the contours in the main image read, just moved to the corresponding coordinates in this image
    # 3: Calls the img_copy method, passing along the cropped image and the contours of the largest object
    def crop_img( self, cnt, img ):
        #Creating bounding rect & grabbing corresponding part of image
        x,y,w,h = cv2.boundingRect(cnt)
        #cropped_img = img[ (y - 50 ):(y+h+50), (x):(x+w+50) ]
        cropped_img = img[ y:y+h, x:x+w ]

        #Moving the contours from the main image to this image ( editing coordinates to fit the smaller image )
        largest = cnt
        for index in range( 0, len( cnt ) ):
            largest[index][0][0] = largest[index][0][0] - x
            largest[index][0][1] = largest[index][0][1] - y

        #Sending cropped image to the img_copy method where the remainder of the processing will occur
        return self.img_copy( cropped_img, largest )

    # Part 2 of the image processing ( part 1 is above )
    # This method accomplishes the following aspects of the image processing:
    # 1: A mask is created the same shape as the cropped image. This mask's background color is black ( this can be edited by editing the properties through the parser object )
    # 2: The object in the image is copied from the image into the cropped image. The cropped image now contains the object in question
    # 3: After that, K-Means clustering is applied for color quantization in the cropped image. The color quantization specifics can be edited by editing the parser's properties
    # 4: Finally, the cropped image is sent to have the image tests completed. If the tests come back true, currently, the image is shown. In the future ( TO DO ), the program will save the object into a file and save the image.
    def img_copy( self, cropped_img, cnt ):
        #Creating a mask & drawing the passed contours onto that mask
        mask_img = np.zeros( cropped_img.shape, dtype=np.uint8 )

        roi_corners = np.array( cnt, dtype=np.int32 )
        white = (255, 255, 255)
        cv2.drawContours( mask_img, [cnt], 0, white, -1 )

        #Copying over the image inside of the contours
        masked_img = cv2.bitwise_and( cropped_img, mask_img )

        #Applying K-Means clustering for color quantization
        Z = masked_img.reshape((-1,3))

        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 3
        ret,label,center=cv2.kmeans(Z,K,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((masked_img.shape))

        #Sending the final image off to be tested to see if it is true or false
        if self.image_tests( res2 ):
            return True

    # Testing the image ( final part of the image processing process )
    # During this function, the following is completed:
    # 1: I get the global setting values. These are threshold values applied when comparing different aspects of the pixels
    # 2: Color test. If the ratios of the colors are not the following, then return the image as a false positive
    #   a: Ratio of Black:Non-Black is greater than 1:1 ( eg, 2:1 )
    #   b: Ratio of Color_1:Color_2 ( non black color comparison ) is less than 1:10, return False. This means that there is too much or too little area covered by the letter on top of the shape
    # 3: Adjacent object test. If there are not 2 non-black colors within a couple of pixels of eachother, return False as the object is a false positive ( for more in depth info, see the comments on the actual process below )
    # 4: Since all of the tests have passed ( if they hadn't they would have stopped executing and returned false ), the method now returns True. This is the end of the image processing for this particular object.
    def image_tests( self, masked_img ):
        #Get global variable settings
        global PIXEL_COLOR_THRESHOLD
        global BLACK_COLOR_THRESHOLD
        global ADJACENT_OBJECT_INDEX

        #Set arrays and other associated required values
        colors = [ [ 0, 0, 0 ] ]
        size = int(masked_img.shape[0]) * int(masked_img.shape[1])
        index = 0

        #Finding the colors in the image. This will allow the ratio test to be completed
        for y in xrange( 0, masked_img.shape[1], 4 ):
            for x in xrange( 0, masked_img.shape[0], 4 ):
                #Getting the current pixel's data
                pixel_data = masked_img[ x, y ]

                #if the pixel data is not black
                if int(pixel_data[0]) > 15 and int(pixel_data[1]) > 15 and int(pixel_data[2]) > 15:
                    #assume the pixel is a new color
                    color_truth = True

                    #if the color is not actually currently in the array, set color_truth to false
                    for color in colors:
                        if ( int(pixel_data[0]) - color[0] < BLACK_COLOR_THRESHOLD and int(pixel_data[0]) - color[0] > -BLACK_COLOR_THRESHOLD ) and ( int(pixel_data[1]) - color[1] < BLACK_COLOR_THRESHOLD and int(pixel_data[1]) - color[1] > -BLACK_COLOR_THRESHOLD ) and ( int(pixel_data[2]) - color[2] < BLACK_COLOR_THRESHOLD and int(pixel_data[2]) - color[2] > -BLACK_COLOR_THRESHOLD ):
                            color_truth = False

                    #if there color is not in the array, add it
                    if color_truth:
                        colors.append( [ int(pixel_data[0]), int(pixel_data[1]), int(pixel_data[2]) ] )

                #print the current status
                #print str( ( ( ( y + 0.0 ) * masked_img.shape[0] ) + x ) * 100 / size ) + "% of Color Test"

            #Since there can not be more than 3 colors ( since K-Means clustering has been applied ), if there are 3, all colors have been found
            if len(colors) == 3:
                break

        #Ratio test
        ratio_index = []
        ratio_index.append( 0 )
        ratio_index.append( 0 )
        ratio_index.append( 0 )

        #Get pixel data
        for y in range( 0, masked_img.shape[1] ):
            for x in range( 0, masked_img.shape[0] ):
                #get pixel data
                pixel_data = masked_img[ x, y ]

                #reseting color index & iterating through the colors array
                color_index = 0
                for color in colors:
                    #if the pixel data equals the color value, add one to that pixel count
                    if int( pixel_data[0] ) == color[0] and int( pixel_data[1] ) == color[1] and int( pixel_data[2] ) == color[2]:
                        ratio_index[ color_index ] += 1

                    #move on to the next color
                    color_index += 1

                #print out the current progress
                #print str( ( ( ( y + 0.0 ) * masked_img.shape[0] ) + x ) * 100 / size ) + "% Completed in determining Ratios"

        #Complete ratio tests
        #If black is greater than the other two colors ( signifying a runway ), return false
        if ratio_index[0] >  ratio_index[1] + ratio_index[2]:
            #print "OBJECT FAILED RATIO TEST"
            return False

        #If the ratio of non-black 1 to non-black 2 colors is < 0.1 ( signifying the area covered is too little or too large )
        if ratio_index[1] > 0 and ratio_index[2] > 0:
            if ratio_index[1] > ratio_index[2]:
                ratio_value = ratio_index[2] * 1.0 / ratio_index[1] * 1.0
                if ratio_value < 0.1:
                    #print "OBJECT FAILED RATIO TEST"
                    return False
            else:
                ratio_value = ratio_index[1] * 1.0 / ratio_index[2] * 1.0
                if ratio_value < 0.1:
                    #print "OBJECT FAILED RATIO TEST"
                    return False

        return True

        # Adjacent object test -- NOTE: THIS IS CURRENTLY DISABLED FOR CAUSING ISSUES WITH OBJECT DETECTION

        # Check every other row, and every third pixel. Ever box, which represents a pixel, that has an X in it is checked by the program
        #  --- --- --- --- --- --- ---
        # | X |   |   | X |   |   | X |
        # |---|---|---|---|---|---|---|
        # |   |   |   |   |   |   |   |
        # |---|---|---|---|---|---|---|
        # | X |   |   | X |   |   | X |
        # |---|---|---|---|---|---|---|
        # |   |   |   |   |   |   |   |
        # |---|---|---|---|---|---|---|
        # | X |   |   | X |   |   | X |
        # |---|---|---|---|---|---|---|
        # |   |   |   |   |   |   |   |
        # |---|---|---|---|---|---|---|
        # | X |   |   | X |   |   | X |
        # |---|---|---|---|---|---|---|
        # |   |   |   |   |   |   |   |
        #  --- --- --- --- --- --- ---
        for y in xrange( 0, masked_img.shape[1], 2 ):
            for x in xrange( 0, masked_img.shape[0], 3 ):
                #Since some of the picked pixels will be out of bounds of the array, a try & catch block has been implemented to remove those issues from crashing the program. Instead, the program just skips the set of pixel that have caused the error.
                try:
                    #Grabbing the pixels to the left 5 pixels and to the right 5 pixels. These 2 lines of code throw index out of bound exceptions ( hence why there is a try and catch block )
                    pixel_value_left = masked_img[x - 5, y ]
                    pixel_value_right = masked_img[ x + 5, y ]

                    #The first if statement tests whether both of the pixels are non-black. This must be true because the background of the picture is black, so it would not work if that black was included in the comparison
                    if int(pixel_value_left[0]) > BLACK_COLOR_THRESHOLD and int(pixel_value_left[1]) > BLACK_COLOR_THRESHOLD and int(pixel_value_left[2]) > BLACK_COLOR_THRESHOLD and int(pixel_value_right[0]) > BLACK_COLOR_THRESHOLD and int(pixel_value_right[1]) > BLACK_COLOR_THRESHOLD and int(pixel_value_right[2]) > BLACK_COLOR_THRESHOLD:
                        #These next 3 if statements determine whether the pixels are the same color. If not, the index value ( instances where there appears to be contrasting colors ) is increased by 1
                        if int(masked_img[ x + 5, y ][0]) - int(masked_img[ x - 5, y ][0]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][0]) - int(masked_img[ x - 5, y ][0]) < -PIXEL_COLOR_THRESHOLD:
                            index += 1
                        elif int(masked_img[ x + 5, y ][1]) - int(masked_img[ x - 5, y ][1]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][1]) - int(masked_img[ x - 5, y ][1]) < -PIXEL_COLOR_THRESHOLD:
                            index += 1
                        elif int(masked_img[ x + 5, y ][2]) - int(masked_img[ x - 5, y ][2]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][2]) - int(masked_img[ x - 5, y ][2]) < -PIXEL_COLOR_THRESHOLD:
                                index += 1
                except:
                    pass

                #Printing the progress of the calculations
                #print str( ( ( ( y + 0.0 ) * masked_img.shape[0] ) + x ) * 100 / size ) + "% of Adjacent Object Test"

        #If there are not ADJACENT_OBJECT_INDEX instances ( eliminating the case where there are a couple of small random occurences of 2 pixels having different color value ), return False
        if index < ADJACENT_OBJECT_INDEX:
            print "OBJECT FAILED ADJACENT OBJECT TEST"
            return False

        #Since all of the tests have passed, return True
        return True

# If this program is specifically called from the command line, execute the following
if __name__ == '__main__':
    parser = image_parser()

    parser.process_img( 'images/IMG_0544.JPG' )

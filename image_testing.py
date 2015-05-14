__author__ = 'Vale'

import numpy as np
import datetime
import cv2

class Image_Parser:
    # These are the global image settings. These are set by specifically referencing them through the parser's properties
    global PIXEL_COLOR_THRESHOLD

    # This method is the initialization method and sets all of the picture settings to default
    def __init__( self, *args, **kwargs ):
        global PIXEL_COLOR_THRESHOLD
        
        PIXEL_COLOR_THRESHOLD = 35

    # Main image processing method. This method will do the following things:
    # 1: Crop the image. This will create the smallest ( almost, with some border ) bounding rectangle around the object in question
    # 2: Find the largest object in the cropped image. Since the cropped image is the bounding rect of the object in question, that object will be the largest object in the image using the contours in the main image read, just moved to the corresponding coordinates in this image
    # 3: Calls the img_copy method, passing along the cropped image and the contours of the largest object
    def process_and_crop_img( self, cnt, img ):
        #Creating bounding rect & grabbing corresponding part of image
        x,y,w,h = cv2.boundingRect(cnt)
        cropped_img = img[ (y - 50 ):(y+h+50), (x):(x+w+50) ]

        #Moving the contours from the main image to this image ( editing coordinates to fit the smaller image )
        largest = cnt
        for index in range( 0, len( cnt ) ):
            largest[index] = largest[index] - x

        #Sending cropped image to the img_copy method where the remainder of the processing will occur
        self.img_copy( cropped_img, largest )

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
        black = (255, 255, 255)
        cv2.drawContours( mask_img, [cnt], 0, black, -1 )
    
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
            #Currently, the image is just being shown if it passes all of the test. In the future, other processes will applied & different actions taken ( TO DO )
            #cv2.imshow( "Image", res2 )
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            pass

    # Testing the image ( final part of the image processing process )
    # During this function, the following is completed:
    # 1: I get the global setting values. These are threshold values applied when comparing different aspects of the pixels
    # 2: Color test. If the ratios of the colors are not the following, then return the image as a false positive ( TO DO )
    #   a: Ratio of Black:Non-Black is less than 1:1 ( eg, 2:1 )
    #   b: Ratio of Color_1:Color_2 ( non black color comparison ) is less than 1:10, return False. This means that there is too much or too little area covered by the letter on top of the shape
    # 3: Adjacent object test. If there are not 2 non-black colors within a couple of pixels of eachother, return False as the object is a false positive ( for more in depth info, see the comments on the actual process below )
    # 4: Since all of the tests have passed ( if they hadn't they would have stopped executing and returned false ), the method now returns True. This is the end of the image processing for this particular object.
    def image_tests( self, masked_img ):
        #Get global variable settings
        global PIXEL_COLOR_THRESHOLD
        
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
                        if ( int(pixel_data[0]) - color[0] < 15 and int(pixel_data[0]) - color[0] > -15 ) and ( int(pixel_data[1]) - color[1] < 15 and int(pixel_data[1]) - color[1] > -15 ) and ( int(pixel_data[2]) - color[2] < 15 and int(pixel_data[2]) - color[2] > -15 ):
                            color_truth = False
                
                    #if there color is not in the array, add it
                    if color_truth:
                        colors.append( [ int(pixel_data[0]), int(pixel_data[1]), int(pixel_data[2]) ] )
        
                #print the current status
                print str( ( ( ( y + 0.0 ) * masked_img.shape[0] ) + x ) * 100 / size ) + "% of Color Test"
            
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
                print str( ( ( ( y + 0.0 ) * masked_img.shape[0] ) + x ) * 100 / size ) + "% Completed in determining Ratios"

        #Complete ratio tests
        #If black is greater than the other two colors ( signifying a runway ), return false
        if ratio_index[0] >  ratio_index[1] + ratio_index[2]:
            return False

        #If the ratio of non-black 1 to non-black 2 colors is < 0.1 ( signifying the area covered is too little or too large )
        if ratio_index[1] > ratio_index[2]:
            ratio_value = ratio_index[2] * 1.0 / ratio_index[1] * 1.0
            if ratio_value < 0.1:
                return False
        else:
            ratio_value = ratio_index[1] * 1.0 / ratio_index[2] * 1.0
            if ratio_value < 0.1:
                return False

        # Adjacent object test
        
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
                    if int(pixel_value_left[0]) > 15 and int(pixel_value_left[1]) > 15 and int(pixel_value_left[2]) > 15 and int(pixel_value_right[0]) > 15 and int(pixel_value_right[1]) > 15 and int(pixel_value_right[2]) > 15:
                        #These next 3 if statements determine whether the pixels are the same color. If not, the index value ( instances where there appears to be contrasting colors ) is increased by 1
                        if int(masked_img[ x + 5, y ][0]) - int(masked_img[ x - 5, y ][0]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][0]) - int(masked_img[ x - 5, y ][0]) < -PIXEL_COLOR_THRESHOLD:
                            if int(masked_img[ x + 5, y ][1]) - int(masked_img[ x - 5, y ][1]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][1]) - int(masked_img[ x - 5, y ][1]) < -PIXEL_COLOR_THRESHOLD:
                                if int(masked_img[ x + 5, y ][2]) - int(masked_img[ x - 5, y ][2]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][2]) - int(masked_img[ x - 5, y ][2]) < -PIXEL_COLOR_THRESHOLD:
                                    index += 1
                                    print "INCREASED INDEX BY +1"
                except:
                    pass
        
                #Printing the progress of the calculations
                print str( ( ( ( y + 0.0 ) * masked_img.shape[0] ) + x ) * 100 / size ) + "% of Adjacent Object Test"

        #If there are not 500 instances ( eliminating the case where there are a couple of small random occurences of 2 pixels having different color value ), return False
        if index < 500:
            return False

        #Since all of the tests have passed, return True
        return True


# This is a temporary test. In the final version, this will be eliminated.

start_time = datetime.datetime.now()

img = cv2.imread( 'images/IMG_0117.jpg' )
img2 = cv2.imread( 'images/IMG_0117.jpg', 0 )
ret,thresh = cv2.threshold(img2,127,255,0)
contours,h = cv2.findContours(thresh,1,2)

my_parser = Image_Parser()

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.007*cv2.arcLength(cnt,True),True)

    if cv2.contourArea(cnt) < 20000 or cv2.contourArea( cnt ) > 50000000:
        pass
    else:
        print len(approx)

        if len(approx)==5:
            print "pentagon"
            
            my_parser.process_and_crop_img( cnt, img )
            
            cv2.drawContours(img,[cnt],0,255,-1)
        elif len(approx)==3:
            print "triangle"
            
            my_parser.process_and_crop_img( cnt, img )
            
            cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        elif len(approx)==4:
            print "square"
            
            my_parser.process_and_crop_img( cnt, img )
            
            cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        elif len(approx) == 9:
            print "complex"
            
            my_parser.process_and_crop_img( cnt, img )
            
            cv2.drawContours(img,[cnt],0,(255,255,0),-1)

#cv2.imshow( "Image", img )
#cv2.waitKey(0)
#cv2.destroyAllWindows()

print datetime.datetime.now() - start_time
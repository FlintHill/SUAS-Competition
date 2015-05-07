import numpy as np
import cv2

img = cv2.imread( 'images/IMG_0117.jpg' )
img2 = cv2.imread( 'images/IMG_0117.jpg', 0 )
ret,thresh = cv2.threshold(img2,127,255,0)
contours,h = cv2.findContours(thresh,1,2)

PIXEL_COLOR_THRESHOLD = 35

def img_copy( cnt ):
    mask_img = np.zeros( img.shape, dtype=np.uint8 )
    roi_corners = np.array( cnt, dtype=np.int32 )
    black = (255, 255, 255)
    cv2.drawContours( mask_img, [cnt], 0, black, -1 )
    
    masked_img = cv2.bitwise_and( img, mask_img )
    
    if test_image( masked_img ):
        cv2.imshow( "Image", masked_img )
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def test_image( masked_img ):
    colors = [ [ 0, 0, 0 ] ]
    size = int(masked_img.shape[0]) * int(masked_img.shape[1])
    index = 0
    
    for y in xrange( 0, masked_img.shape[1], 4 ):
        for x in xrange( 0, masked_img.shape[0], 4 ):
            pixel_data = masked_img[ x, y ]

            if int(pixel_data[0]) > 15 and int(pixel_data[1]) > 15 and int(pixel_data[2]) > 15 and int(pixel_data[0]) > 15 and int(pixel_data[1]) > 15 and int(pixel_data[2]) > 15:
                color_truth = True
            
                for color in colors:
                    if ( int(pixel_data[0]) - color[0] < 15 or int(pixel_data[0]) - color[0] > -15 ) and ( int(pixel_data[1]) - color[1] < 15 or int(pixel_data[1]) - color[1] > -15 ) and ( int(pixel_data[2]) - color[2] < 15 or int(pixel_data[2]) - color[2] > -15 ):
                        color_truth = False
        
                if color_truth:
                    colors.append( [ int(pixel_data[0]), int(pixel_data[1]), int(pixel_data[2]) ] )

            print str( ( ( ( y + 0.0 ) * img.shape[0] ) + x ) * 100 / size ) + "% of Color Test"

            if len(colors) > 4:
                return False

    print colors
    cv2.waitKey(0)

    for y in xrange( 0, masked_img.shape[1], 3 ):
        for x in xrange( 0, masked_img.shape[0], 3 ):
            try:
                pixel_value_left = masked_img[x - 5, y ]
                pixel_value_right = masked_img[ x + 5, y ]
           
                if int(pixel_value_left[0]) > 15 and int(pixel_value_left[1]) > 15 and int(pixel_value_left[2]) > 15 and int(pixel_value_right[0]) > 15 and int(pixel_value_right[1]) > 15 and int(pixel_value_right[2]) > 15:
                   if int(masked_img[ x + 5, y ][0]) - int(masked_img[ x - 5, y ][0]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][0]) - int(masked_img[ x - 5, y ][0]) < -PIXEL_COLOR_THRESHOLD:
                       if int(masked_img[ x + 5, y ][1]) - int(masked_img[ x - 5, y ][1]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][1]) - int(masked_img[ x - 5, y ][1]) < -PIXEL_COLOR_THRESHOLD:
                           if int(masked_img[ x + 5, y ][2]) - int(masked_img[ x - 5, y ][2]) > PIXEL_COLOR_THRESHOLD or int(masked_img[ x + 5, y ][2]) - int(masked_img[ x - 5, y ][2]) < -PIXEL_COLOR_THRESHOLD:
                               index += 1
            except:
                pass

            print str( ( ( ( y + 0.0 ) * img.shape[0] ) + x ) * 100 / size ) + "% of Adjacent Object Test"
    
    if index > 500:
        return True

    return False

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.007*cv2.arcLength(cnt,True),True)

    if cv2.contourArea(cnt) < 20000 or cv2.contourArea( cnt ) > 50000000:
        pass
    else:
        print len(approx)

        if len(approx)==5:
            print "pentagon"
            
            img_copy( cnt )
            
            cv2.drawContours(img,[cnt],0,255,-1)
        elif len(approx)==3:
            print "triangle"
            
            img_copy( cnt )
            
            cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        elif len(approx)==4:
            print "square"
            
            img_copy( cnt )
            
            cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        elif len(approx)==5:
            print "pentagon"
            
            img_copy( cnt )
            
            cv2.drawContours(img,[cnt],0,(0,0,127),-1)
        elif len(approx) == 9:
            print "complex"
            
            img_copy( cnt )
            
            cv2.drawContours(img,[cnt],0,(255,255,0),-1)

cv2.imshow( "Image", img )
cv2.waitKey(0)
cv2.destroyAllWindows()
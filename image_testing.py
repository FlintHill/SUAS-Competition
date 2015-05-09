import numpy as np
import cv2

img = cv2.imread( 'images/IMG_0117.jpg' )
img2 = cv2.imread( 'images/IMG_0117.jpg', 0 )
ret,thresh = cv2.threshold(img2,127,255,0)
contours,h = cv2.findContours(thresh,1,2)

PIXEL_COLOR_THRESHOLD = 35

def cropped_img_finding( cnt ):
    x,y,w,h = cv2.boundingRect(cnt)
    cropped_img = img[ (y - 50 ):(y+h+50), (x):(x+w+50) ]

    largest = cnt
    for index in range( 0, len( cnt ) ):
        largest[index] = largest[index] - x #( x - 50 )

    img_copy( cropped_img, largest )

def img_copy( cropped_img, cnt ):
    mask_img = np.zeros( cropped_img.shape, dtype=np.uint8 )
    roi_corners = np.array( cnt, dtype=np.int32 )
    black = (255, 255, 255)
    cv2.drawContours( mask_img, [cnt], 0, black, -1 )
    
    masked_img = cv2.bitwise_and( cropped_img, mask_img )
    
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
    
    if test_image( res2 ):
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

            if int(pixel_data[0]) > 15 and int(pixel_data[1]) > 15 and int(pixel_data[2]) > 15:
                color_truth = True
            
                for color in colors:
                    if ( int(pixel_data[0]) - color[0] < 15 and int(pixel_data[0]) - color[0] > -15 ) and ( int(pixel_data[1]) - color[1] < 15 and int(pixel_data[1]) - color[1] > -15 ) and ( int(pixel_data[2]) - color[2] < 15 and int(pixel_data[2]) - color[2] > -15 ):
                        color_truth = False
        
                if color_truth:
                    colors.append( [ int(pixel_data[0]), int(pixel_data[1]), int(pixel_data[2]) ] )

            print str( ( ( ( y + 0.0 ) * masked_img.shape[0] ) + x ) * 100 / size ) + "% of Color Test"

            if len(colors) > 3:
                return False

    for y in xrange( 0, masked_img.shape[1], 1 ):
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

            print str( ( ( ( y + 0.0 ) * masked_img.shape[0] ) + x ) * 100 / size ) + "% of Adjacent Object Test"

    if index < 500:
        return False

    return True

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.007*cv2.arcLength(cnt,True),True)

    if cv2.contourArea(cnt) < 20000 or cv2.contourArea( cnt ) > 50000000:
        pass
    else:
        print len(approx)

        if len(approx)==5:
            print "pentagon"
            
            cropped_img_finding( cnt )
            
            cv2.drawContours(img,[cnt],0,255,-1)
        elif len(approx)==3:
            print "triangle"
            
            cropped_img_finding( cnt )
            
            cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        elif len(approx)==4:
            print "square"
            
            cropped_img_finding( cnt )
            
            cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        elif len(approx) == 9:
            print "complex"
            
            cropped_img_finding( cnt )
            
            cv2.drawContours(img,[cnt],0,(255,255,0),-1)

cv2.imshow( "Image", img )
cv2.waitKey(0)
cv2.destroyAllWindows()
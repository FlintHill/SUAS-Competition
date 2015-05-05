import numpy as np
import cv2

img = cv2.imread( 'images/IMG_0119.jpg' )
img2 = cv2.imread( 'images/IMG_0119.jpg', 0 )
ret,thresh = cv2.threshold(img2,127,255,0)
contours,h = cv2.findContours(thresh,1,2)

def img_copy( cnt ):
    mask_img = np.zeros( img.shape, dtype=np.uint8 )
    roi_corners = np.array( cnt, dtype=np.int32 )
    black = (255, 255, 255)
    cv2.drawContours( mask_img, [cnt], 0, black, -1 )
    
    masked_img = cv2.bitwise_and( img, mask_img )
    
    cv2.imshow( "Image", masked_img )
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return test_image( masked_img )

def test_image( masked_img ):
    return True

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.007*cv2.arcLength(cnt,True),True)

    if cv2.contourArea(cnt) < 20000:
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
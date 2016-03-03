import numpy as np
import cv2

img = cv2.imread( '../images/IMG_0160.JPG' )

cv2.imshow( "Original", img )
cv2.waitKey( 0 )
cv2.destroyAllWindows()

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
smoothed = cv2.cvtColor( hsv, cv2.COLOR_BGR2GRAY )

cv2.imshow( "Smoothed", smoothed )
cv2.waitKey( 0 )
cv2.destroyAllWindows()

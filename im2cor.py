############################################################################
# This file is only an example of the star detection procedure that will   #
# take place                     					   #
############################################################################

import numpy as np
import cv2
import math

# Load an example image from ISS in grayscale 
# http://spaceflight.nasa.gov/gallery/images/station/crew-6/hires/iss006e40544.jpg
i = cv2.imread('iss006e40544.jpg',0)

img = i[1:1200, 1:2000] # Do some crop under to remove the iss image code

median1 = cv2.medianBlur(img,5)
cv2.imwrite('iss006e40544_median1.png',median1)

median2 = cv2.medianBlur(median1,5)
cv2.imwrite('iss006e40544_median2.png',median2)

ret,thresh1 = cv2.threshold(median2,110,255,cv2.THRESH_BINARY)
cv2.imwrite('iss006e40544_otsu.png',thresh1)

detector = cv2.SimpleBlobDetector()
keypoints = detector.detect(255-thresh1)

font = cv2.FONT_HERSHEY_SIMPLEX
for s,kp in enumerate(keypoints):
	x, y = kp.pt  
	#print (x, y)
	cv2.circle(img,(int(x),int(y)),20 , (255,0,255),1 )
	cv2.putText(img,str(s),(int(x)-22,int(y)-22), font, 0.6,(255,255,255))
cv2.imwrite('iss006e40544_circles.png',img)

# compute angular distances 
# (for geometrical corrected image)
r = 9850  # r is a factor that must be calibrated to the corresponding image
for s1,kp1 in enumerate(keypoints):
	for s2,kp2 in enumerate(keypoints):
	 	if kp1<kp2:
			x1, y1 = kp1.pt
			x2, y2 = kp2.pt
			d = math.sqrt((x1-x2)**2+(y1-y2)**2)
			phi = 2*math.asin(2*d/r)
			print s1,s2,phi*180/math.pi # Show results in degrees 
